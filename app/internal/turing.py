import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import pkcs12
from sqlalchemy.orm import Session
from app.internal.ApiCommons import ApiCommons
from app.db.DynamoDB import DynamoDB
from app.schemas.pan import GetCustomerIdRequestSchema
from app.schemas.turing import CustomerOnboardingRequest
from app.config.turing import config
from app.base.aws import S3Service
from app.repository.session import create_session_data


class TuringAPI(ApiCommons):
	"""Class for Turing API logic"""

	"""
	TODO:
	1. Customer Onboarding
	2. Photo Upload
	3. Signature Upload
	"""

	ApiBASE = config.customer_onboarding_base_url
	ApiGetCustomerIdByAadhar = config.get_customer_by_aadhaar_api_endpoint
	ApiGetCustomerDetails = config.get_customer_details_api_endpoint
	ApiGetPickList = config.get_pick_list_api_endpoint
	ApiCustomerOnboarding =  config.customer_onboarding_api_endpoint
	CertificateStorage = "S3"
	CertificatePath = config.dsc_key
	Password = config.dsc_password
	XKey = config.application_key
	Headers = {"Accept": "application/json", "Content-Type": "application/json"}
	TAG_CUSTOMER_ONBOARDING_REQUEST = "turing.customer_onboarding.request"
	TAG_CUSTOMER_ONBOARDING_RESPONSE = "turing.customer_onboarding.response"

	@classmethod
	async def customer_onboarding(cls,db:Session,session_id:str):
		"""
		Class method that makes async request to Turing API ApiCustomerOnboarding

		:param db: db session from dependency injection on the route
		:param session_id: session id from authenticated user (global dependency)
		:return: Response JSON from the onboarding API
		"""
		onboarding_request = cls.check_session_data(db=db,session_id=session_id,_tag=cls.TAG_CUSTOMER_ONBOARDING_REQUEST)
		if not onboarding_request:
			return {"error":f"No data for {cls.TAG_CUSTOMER_ONBOARDING_REQUEST} found"}
		response_payload = await cls.make_async_request(
			"POST",
			cls.ApiCustomerOnboarding,
			payload=CustomerOnboardingRequest(**onboarding_request).model_dump()
			)
		create_session_data(
			db=db,
			session_id=session_id,
			tag=cls.TAG_CUSTOMER_ONBOARDING_REQUEST,
			data=response_payload,
		)
		return response_payload

	@classmethod
	async def get_customer_id_by_pan_aadhar(
		cls, aadhar_card: str = None, pan_card: str = None
	) -> dict:
		"""
		Class method that makes async request to Turing API ApiGetCustomerIdByAadhar

		:param aadhar_card: aadharCard json param for the Turing API, optional
		:param pan_card: panCard json param for the Turing API, optional
		:return: Response JSON of user record (empty list if no records found)
		"""
		# dynamo = DynamoDB()
		# existing_record = dynamo.AadharPanTable.get_item(Key={"pan":pan_card})
		# if existing_record.get('Item'): #and existing_record.get('Item').get('aadhar')==aadhar_card:
		#     return  existing_record.get('Item')
		payload = None
		if aadhar_card:
			payload = GetCustomerIdRequestSchema(aadharCard=aadhar_card)
		elif pan_card:
			payload = GetCustomerIdRequestSchema(panCard=pan_card)
		else:
			return {"error": "input required - pan or aadhar"}
		url = "".join([cls.ApiBASE, cls.ApiGetCustomerIdByAadhar])
		api_response = await cls.make_async_request(
			"POST", url, payload=payload.json()
		)  # .model_dump(mode='json')
		user_record = dict()
		for user_id in api_response.get("results", []):
			user_record = {"user_id": user_id, "aadhar": aadhar_card, "pan": pan_card}
			# dynamo.AadharPanTable.put_item(Item=user_record)
		return user_record

	@classmethod
	async def get_customer_details(cls, customer_id: str) -> dict:
		"""
		Class method that makes async request to Turing API ApiGetCustomerDetails

		:param customer_id: customer id param for the Turing API
		:return: Response JSON of customer details
		"""
		dynamo = DynamoDB()
		existing_record = dynamo.TuringCustomerDetailsTable.get_item(
			Key={"customer_id": customer_id}
		)
		record = existing_record.get("Item")
		if record:
			return record["results"]
		api_response = await cls.make_async_request(
			"GET", cls.ApiGetCustomerDetails + customer_id
		)
		api_results = {"results": api_response["results"]}
		api_results["customer_id"] = customer_id
		dynamo.TuringCustomerDetailsTable.put_item(Item=api_results)
		return api_results["results"]

	@classmethod
	async def get_pick_list(cls, typeCode: str, orderBy: str = "C") -> dict:
		"""
		Class method that makes async request to Turing API ApiGetPickList

		:param typeCode: type code param for the Turing API
		:param orderBy: order by param for the Turing API, default value 'C'
		:return: Response JSON of pick list
		"""
		# dynamo = DynamoDB()
		# existing_record = dynamo.PickListTable.get_item(Key={"typeCode": typeCode})
		# record = existing_record.get("Item")
		# if record:
		#     return record["results"]
		url = "".join(
			[cls.ApiBASE, cls.ApiGetPickList.format(typeCode=typeCode, orderBy=orderBy)]
		)
		message = url.split("?")[1]
		headers = {"x-key": cls.XKey, "signed-data": cls.sign(message)}
		api_response = await cls.make_async_request("GET", url, custom_headers=headers)
		api_results = {"results": api_response["results"]}
		api_results["typeCode"] = typeCode
		# dynamo.PickListTable.put_item(Item=api_results)
		return api_results["results"]

	@classmethod
	async def token_creation_method(cls) -> None:
		pass

	@classmethod
	def sign(cls, message: str):
		if cls.CertificateStorage == "S3":
			s3 = S3Service()
			pfx_data = s3.get_file(config.s3_bucket_name, cls.CertificatePath)
		else:
			with open(cls.CertificatePath, mode="rb") as pfx_f:
				pfx_data = pfx_f.read()

		private_key = pkcs12.load_key_and_certificates(
			pfx_data, cls.Password.encode("utf-8")
		)[0]
		message_bytes = message.encode("utf-8")
		# Sign the message
		signature = private_key.sign(message_bytes, padding.PKCS1v15(), hashes.SHA256())
		# Encode the signature in base64
		return base64.b64encode(signature).decode("utf-8")

	@classmethod
	def create_request_headers(cls, payload: dict) -> dict:
		"""
		Class method that makes

		:param payload: payload that needs to be signed with pfx certificate and password
		:return: dict with headers that includes x-key with signed payload
		"""
		encoded_signature = cls.sign(str(payload))
		headers = cls.Headers.copy()
		headers["x-key"] = cls.XKey
		headers["signed-data"] = encoded_signature
		return headers

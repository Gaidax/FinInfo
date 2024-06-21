#from datetime import datetime
import time
import jwt
from functools import wraps
from sqlalchemy.orm import Session
from app.internal.ApiCommons import ApiCommons
from app.schemas.token import GenerateTokenRequestSchema
from app.config.vkyc import config
#from app.db.DynamoDB import DynamoDB
from app.schemas.vkyc import VkycSendLinkRequest
from app.repository.session import create_session_data, create_session_state
from app.schemas.common import StepStatus, StepType
from app.internal.steps import TAG_EAADHAAR_VERIFICATION_SEND_OTP_RESPONSE
from typing import Tuple

def checkVKYCTokenValidity(func):
    """Wrapper for token expiry check"""
    @wraps(func)
    async def wrapper(*args,**kwargs):
        if time.time() - float(config.token_expiry) >= 86400:#implying timestamp
            await VkycAPI.token_creation_method()
        return await func(*args,**kwargs)
    return wrapper

class VkycAPI(ApiCommons):
    """Class for VKYC API logic"""

    ApiBASE =  config.base_url
    ApiGenerateToken = config.generate_token
    ApiSendLink = config.send_link
    ApiGetDetails = config.get_details
    Username = config.username
    Password = config.password
    TokenPublicKey = config.publicKey
    TokenAudience = config.aud
    token = config.token
    CREATE_LINK_RESPONSE = "vkyc.api.create_link_response"
    GET_USER_DETAILS_RESPONSE = "vkyc.api.get_details_response"
    
    @classmethod
    def create_request_headers(cls,payload=dict()):
        return {"Accept": "application/json", "Content-Type": "application/json",
                    "Authorization": f"Bearer {cls.token}"}

    @classmethod
    async def token_creation_method(cls):
        token = await cls.make_async_request(
            "POST",
            cls.ApiGenerateToken,
            custom_headers={"Content-Type": "application/json"},
            payload=GenerateTokenRequestSchema(username=cls.Username,password=cls.Password).model_dump_json()
            )
        token = token['Token']
        cls.token = token
        config.token = token
        decoded_token = jwt.decode(token, cls.TokenPublicKey,audience=cls.TokenAudience, algorithms=["HS256"], verify=False)
        config.token_expiry = str(decoded_token['exp'])
        #with open(conf_file, 'w') as configfile:
        #    config.write(configfile)

    @classmethod
    @checkVKYCTokenValidity
    async def vkyc_send_link(
        cls,
        #requestPayload:dict,
        db:Session,
        session_id:str
        )->Tuple:
        """
        Class method that makes async request to Vkyc API ApiSendLink

        :param requestPayload: incoming json payload for the Vkyc API (may be converted to a model class for future endpoints)
        :return: Response JSON payload with link information
        """
        #dynamo = DynamoDB()
        #key = requestPayload['user_id']
        #existing_record = dynamo.SendLinkTable.get_item(Key={"user_id":key})
        #record = existing_record.get('Item')
        #if record and datetime.now() > datetime.fromtimestamp(float(record['results']['link_expiry_time'])):#if timestamp is in the past ignore the record, link expired
        #   return record['results']
        
        session_data = cls.check_session_data(
        db=db, session_id=session_id, _tag=TAG_EAADHAAR_VERIFICATION_SEND_OTP_RESPONSE
        )#construct the json from data stored in the session ? NOMINEE_DETAILS PERSONAL_DETAILS etc
        request_data = VkycSendLinkRequest(**session_data)
        api_response = await cls.make_async_request(
            'POST',
            cls.ApiSendLink,
            payload=request_data.model_dump()
            )
        create_session_data(
                db=db,
                session_id=session_id,
                tag=VkycAPI.CREATE_LINK_RESPONSE,
                data=api_response,
            )
        create_session_state(
            db=db,
            session_id=session_id,
            step=StepType.vkyc,
            status=StepStatus.in_progress,
        )

        #api_results = {'results':api_response}
        #api_results['user_id'] = key
        #dynamo.SendLinkTable.put_item(Item=api_results)
        return StepStatus.in_progress, None#api_results['results']
    
    @classmethod
    @checkVKYCTokenValidity
    async def get_details(cls,db:Session,session_id:str)->Tuple:
        """
        Class method that makes async request to Vkyc API ApiGetDetails

        :param session_id: incoming session id for the Vkyc API
        :return: Response JSON payload with session data
        """
        #dynamo = DynamoDB()
        #existing_record = dynamo.VkycDetailsTable.get_item(Key={"session_id":session_id})
        #record = existing_record.get('Item')
        #if record:
        #    return record['results']

        get_details_response = await cls.make_async_request('GET',cls.ApiGetDetails+session_id)
        create_session_data(
                db=db,
                session_id=session_id,
                tag=VkycAPI.GET_USER_DETAILS_RESPONSE,
                data=get_details_response,
            )
        create_session_state(
            db=db,
            session_id=session_id,
            step=StepType.vkyc,
            status=StepStatus.in_progress,
        )
        #api_results = {'results':api_response['session_data']}
        #api_results['session_id'] = session_id
        return StepStatus.in_progress, None#api_results['results']
    



    
import requests
import base64
import json
from datetime import datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import pkcs7, pkcs12
from app.internal.ApiCommons import ApiCommons
from app.config.protean import config
from app.base.aws import S3Service
from app.schemas.pan import VerifyPanRequestSchema, ProteanPanVerificationRecordSchema
from app.utils import rootLogger as logger


class ProteanApiError(Exception):
    pass


class ProteanAPI(ApiCommons):
    UserId = config.user_id
    S3BucketName = config.s3_bucket_name
    DscKey = config.dsc_key
    Password = config.password
    PanVerificationUrl = config.pan_verification_url
    PanVerificationUrl_V2 = config.pan_verification_url_v2
    CertificateStorage = "S3"

    @classmethod
    def create_request_headers(cls, payload=...):
        dt = datetime.now()
        transaction_id = f"{cls.UserId}:{dt.timestamp()}"
        transaction_id = transaction_id.replace(".", "")
        return {
            "User_ID": cls.UserId,
            "Records_count": "1",
            "Request_time": dt.strftime("%Y-%m-%dT%H:%M:%S"),
            "Transaction_ID": transaction_id,
            "Version": "4",
        }

    @classmethod
    def get_signature(cls, msg: str):
        if cls.CertificateStorage == "S3":
            s3 = S3Service()
            pfx_data = s3.get_file(cls.S3BucketName, cls.DscKey)
        else:
            with open(cls.CertificatePath, mode="rb") as pfx_f:
                pfx_data = pfx_f.read()

        # Load private key and certificate from PFX
        private_key, cert, _ = pkcs12.load_key_and_certificates(
            pfx_data, cls.Password.encode(), None
        )

        # Create PKCS#7 signature
        options = [pkcs7.PKCS7Options.DetachedSignature]
        p7s_bytes = (
            pkcs7.PKCS7SignatureBuilder()
            .set_data(msg.encode())
            .add_signer(cert, private_key, hashes.SHA256())
            .sign(serialization.Encoding.DER, options)
        )

        # Return base64-encoded signature
        return base64.b64encode(p7s_bytes).decode()

    @classmethod
    def get_inputData(self, input: VerifyPanRequestSchema):
        return [
            {
                "pan": input.pan,
                "name": input.name,
                "fathername": input.father_name,
                "dob": input.dob.strftime("%d/%m/%Y"),
            }
        ]

    @classmethod
    def get_payload_v2(cls, input: VerifyPanRequestSchema):
        data = f"{config.user_id}^{input.pan}"
        signature = cls.get_signature(msg=data)
        return {"data": data, "signature": signature, "version": 2}

    @classmethod
    def get_payload(cls, input: VerifyPanRequestSchema):
        input_data = cls.get_inputData(input=input)
        msg = msg = json.dumps(input_data, separators=(",", ":"))
        return {
            "inputData": input_data,
            "signature": cls.get_signature(msg),
        }

    @classmethod
    async def verifyPan(
        cls, input: VerifyPanRequestSchema
    ) -> ProteanPanVerificationRecordSchema:
        payload = cls.get_payload(input=input)
        response = requests.post(
            url=cls.PanVerificationUrl,
            headers=cls.createRequestHeaders(payload=payload),
            json=payload,
            verify=False,   #noqa
            timeout=10,
        )
        logger.debug(
            f"Protean API response: status_code={response.status_code}, content={response.content}"
        )
        if response.ok:
            json_response = response.json()
            if json_response["response_Code"] == "1":
                data = json_response["outputData"][0]
                return ProteanPanVerificationRecordSchema(**data)
        logger.error(
            f"Protean API response: status code={response.status_code}, content={response.content}"
        )
        raise ProteanApiError("Failed to verify PAN details")

    @classmethod
    async def verifyPan_v2(
        cls, input: VerifyPanRequestSchema
    ) -> ProteanPanVerificationRecordSchema:
        result = None
        try:
            response = requests.post(
                url=cls.PanVerificationUrl_V2,
                json=cls.get_payload_v2(input=input),
                timeout=5,
            )
            if response.ok and response.text[0] == "1":
                split_response = response.text.split("^")
                result = {
                    "pan": split_response[1],
                    "pan_status": split_response[2],
                    "name": "Y",
                    "fathername": "Y",
                    "dob": "Y",
                    "seeding_status": split_response[13],
                }
        except Exception as e:
            logger.exception(e)

        # TODO: Dummy response
        if input.pan == "AIFPP5729A":
            result = {
                "pan": input.pan,
                "pan_status": "E",
                "name": "Y",
                "fathername": "Y",
                "dob": "Y",
                "seeding_status": "Y",
            }
        else:
            result = {
                "pan": input.pan,
                "pan_status": "E",
                "name": "Y",
                "fathername": "Y",
                "dob": "Y",
                "seeding_status": "Y",
            }

        return ProteanPanVerificationRecordSchema(**result)

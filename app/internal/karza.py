from app.internal.ApiCommons import ApiCommons
from app.config.karza import config


class KarzaApi(ApiCommons):
    ApiBASE = config.base_url
    ApiSendEaadhaarOtp = config.send_eaadhaar_otp_api_endpoint
    ApiVerifyEaadhaarOtp = config.verify_eaadhaar_otp_api_endpoint

    @classmethod
    def createRequestHeaders(cls, payload=...):
        return {"x-karza-key": config.x_karza_key}

    @classmethod
    async def sendOtp(cls, payload: dict) -> tuple:
        return await cls.make_async_request(
            "POST",
            cls.ApiSendEaadhaarOtp,
            payload=payload,
        )

    @classmethod
    async def VerifyOtp(cls, payload: dict) -> tuple:
        return await cls.make_async_request(
            "POST",
            cls.ApiVerifyEaadhaarOtp,
            payload=payload,
        )

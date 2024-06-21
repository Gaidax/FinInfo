import random
import string
from sqlalchemy.orm import Session
from app.internal.ApiCommons import ApiCommons
from app.schemas.orck import RiskRatingCalculationAPIRequest
from app.repository.session import create_session_data
from app.config.orck import config
#from app.db.DynamoDB import DynamoDB


class OrckAPI(ApiCommons):
    """Class for ORCK API logic"""
    ApiBASE = config.base_url
    ApiOrckRiskRatingCalculation = config.risk_rating_calculation
    TAG_RISK_RATING_REQUEST = "orck.risk_rating.request"
    TAG_RISK_RATING_ORCK_RESPONSE = "orck.risk_rating.response"

    @classmethod
    async def token_creation_method(cls)->None:
        pass
  
    @classmethod
    def create_request_headers(cls,payload:dict)->None:
        pass

    @classmethod
    async def risk_rating_calculation(cls,db:Session,session_id:str):
        """
        Class method that makes async request to ORCK API ApiOrckRiskRatingCalculation

        :param session_id: id of user session with stored request paramaters in DynamoDB
        :return: Response JSON of user record and weather user is a returning user (record exists in DynamoDB table)
        """

        riskratingcalc = cls.check_session_data(db=db,session_id=session_id,_tag=cls.TAG_RISK_RATING_REQUEST)
        if not riskratingcalc:
            return {"error":f"No {cls.TAG_RISK_RATING_REQUEST} data found "}
        riskratingcalc['requestId'] = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        response_payload = await cls.make_async_request(
            "POST",
            cls.ApiOrckRiskRatingCalculation,
            payload=RiskRatingCalculationAPIRequest(**riskratingcalc).model_dump(),
            )
        create_session_data(
            db=db,
            session_id=session_id,
            tag=cls.TAG_RISK_RATING_ORCK_RESPONSE,
            data=response_payload,
        )
        return
        

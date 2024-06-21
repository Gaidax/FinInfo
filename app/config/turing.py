from functools import lru_cache
from pydantic_settings import BaseSettings
from app.config.base import get_ssm_param_value_as_json


class Config(BaseSettings):
    customer_onboarding_base_url: str
    get_customer_by_aadhaar_api_endpoint: str
    get_customer_details_api_endpoint: str
    get_pick_list_api_endpoint: str
    customer_onboarding_api_endpoint: str
    s3_bucket_name: str
    dsc_key: str
    dsc_password: str
    application_key: str
    


@lru_cache
def get_config():
    data = get_ssm_param_value_as_json("turing")

    #from app.utils import config

    #data={
    #"customer_onboarding_base_url": "str",
    #"get_customer_by_aadhaar_api_endpoint": config["TuringAPI"]["api.turing.getCustomerIdByAadhar"],
    #"get_customer_details_api_endpoint": config["TuringAPI"]["api.turing.get_customer_details"],
    #"get_pick_list_api_endpoint": config["TuringAPI"]["api.turing.get_pick_list"],
    #"customer_onboarding_api_endpoint": config["TuringAPI"]["api.turing.cutsomer_onboarding"],
    #"s3_bucket_name": "str",
    #"dsc_key": "str",
    #"dsc_password": "str",
    #"application_key": "st"
    #}

    return Config(**data)


config = get_config()

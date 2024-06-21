from functools import lru_cache
from pydantic_settings import BaseSettings
from app.config.base import get_ssm_param_value_as_json


class Config(BaseSettings):
    base_url: str
    send_eaadhaar_otp_api_endpoint: str
    verify_eaadhaar_otp_api_endpoint: str
    x_karza_key: str


@lru_cache
def get_config():
    data = get_ssm_param_value_as_json("karza")
    #data = {
    #"base_url": "str",
    #"send_eaadhaar_otp_api_endpoint": "str",
    #"verify_eaadhaar_otp_api_endpoint": "str",
    #"x_karza_key": "str"       
    #}
    return Config(**data)


config = get_config()

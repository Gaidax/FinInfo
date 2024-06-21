from functools import lru_cache
from pydantic_settings import BaseSettings
from app.config.base import get_ssm_param_value_as_json


class Config(BaseSettings):
    base_url: str
    create_token_api_endpoint: str
    screening_api_endpoint: str
    username: str
    password: str
    client_id: str
    client_secret: str
    business_unit: str
    request_type: str
    sub_business_unit: str
    token: str | None = None


@lru_cache
def get_config():
    data = get_ssm_param_value_as_json("ramp")
    #from app.utils import config
    #data = {
    #"base_url": "http://127.0.0.1:8080/",
    #"create_token_api_endpoint": config["RampAPI"]["api.ramp.createToken"],
    #"screening_api_endpoint": config["RampAPI"]["api.ramp.Screening"],
    #"username": "str",
    #"password": "str",
    #"client_id": "str",
    #"client_secret": "str",
    #"business_unit": "str",
    #"request_type": "str",
    #"sub_business_unit": "str",
    #"token": config["RampAPI"]["api.ramp.token"]
    #}

    return Config(**data)


config = get_config()

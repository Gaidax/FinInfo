from functools import lru_cache
from pydantic_settings import BaseSettings
from app.config.base import get_ssm_param_value_as_json


class Config(BaseSettings):
    pan_verification_url_v2: str
    pan_verification_url: str
    user_id: str
    password: str
    s3_bucket_name: str
    dsc_key: str


@lru_cache
def get_config():
    data = get_ssm_param_value_as_json("protean")
    #data = {    "pan_verification_url_v2": "str",
    #"pan_verification_url": "str",
    #"user_id": "str",
    #"password": "str",
    #"s3_bucket_name": "str",
    #"dsc_key": "str"}
    return Config(**data)


config = get_config()

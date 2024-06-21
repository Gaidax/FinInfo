from functools import lru_cache
from pydantic_settings import BaseSettings
from app.config.base import get_ssm_param_value_as_json


class Config(BaseSettings):
    base_url: str
    insert_api_endpoint: str
    get_by_refid_api_endpoint: str
    get_by_refdata_api_endpoint: str


@lru_cache
def get_config():
    data = get_ssm_param_value_as_json("vault")
    #data = {    "base_url": "str",
    #"insert_api_endpoint": "str",
    #"get_by_refid_api_endpoint": "str",
    #"get_by_refdata_api_endpoint": "str"}
    return Config(**data)


config = get_config()

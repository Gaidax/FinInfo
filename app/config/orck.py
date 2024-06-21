from functools import lru_cache
from pydantic_settings import BaseSettings
from app.config.base import get_ssm_param_value_as_json


class Config(BaseSettings):
    base_url: str
    risk_rating_calculation:str


@lru_cache
def get_config():
    data = get_ssm_param_value_as_json("vkyc")

    #from app.utils import config

    #data = {
    #"base_url": config['OrckAPI']['api.orck.base'],
    #"risk_rating_calculation":config['OrckAPI']['api.orck.risk_rating_calculation']
    #}

    return Config(**data)


config = get_config()

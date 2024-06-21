from functools import lru_cache
from pydantic_settings import BaseSettings
from app.config.base import get_ssm_param_value_as_json


class Config(BaseSettings):
    base_url: str
    username: str
    password: str
    generate_token: str
    send_link: str
    get_details: str
    publicKey: str
    aud: str
    token_expiry: str | None = None
    token: str | None = None


@lru_cache
def get_config():
    data = get_ssm_param_value_as_json("vkyc")

    #from app.utils import config

    #data = {
    #"base_url": "http://127.0.0.1:8080/",#config["VkycAPI"]["api.vkyc.generateToken"],
    #"username": config["VkycAPI"]["api.vkyc.username"],
    #"password": config["VkycAPI"]["api.vkyc.password"],
    #"generate_token": config["VkycAPI"]["api.vkyc.generateToken"],
    #"send_link": config["VkycAPI"]["api.vkyc.api.sendLink"],
    #"get_details": config["VkycAPI"]["api.vkyc.getdetails"],
    #"publicKey": config["VkycAPI"]["api.vkyc.token.publickey"],
    #"aud": config["VkycAPI"]["api.vkyc.token.aud"],
    #"token_expiry": config["VkycAPI"]["api.vkyc.token.expiry"],
    #"token": config["VkycAPI"]["api.vkyc.token"]
    #}

    return Config(**data)


config = get_config()

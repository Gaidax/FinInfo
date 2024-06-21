import os
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(__file__), ".env")

class Settings(BaseSettings):
    #base_ssm_parameter_name: str
    #aws_region: str
    #aws_access_key: str
    #aws_secret_access_key: str
    database_url: str
    log2file: bool = False

    model_config = SettingsConfigDict(env_file=DOTENV)


settings = Settings()

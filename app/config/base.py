import json
from app.base.aws import SSMParamStore
from app.utils import rootLogger as logger
from app.config import settings


class BaseConfig:

    def __init__(self, path) -> None:
        self.path = path

    def get_client(self):
        return SSMParamStore()

    def get_value(self, name):
        key = f"{self.path}/{name}"
        param_store = self.get_client()
        return param_store.get_param_value(key)

    def set_value(self, name, value, type):
        key = f"{self.path}/{name}"
        param_store = self.get_client()
        return param_store.set_param_value(param=key, value=value, type=type)

    def get_values(self, name):
        key = f"{self.path}/{name}"
        param_store = self.get_client()
        return param_store.get_param_values(key)


class BaseJsonConfig(BaseConfig):
    def __init__(self, path, json_key) -> None:
        super().__init__(path=path)
        self.json_key = json_key

    def json(self):
        value = self.get_value(self.json_key)
        if not value:
            raise Exception(f"No value found for key: {self.json_key}")
        result = None
        try:
            result = json.loads(value)
        except Exception:
            logger.error(f"Error loading value: {value}")
            raise
        return result


def get_ssm_param_value_as_json(key):
    config = BaseJsonConfig(path=settings.base_ssm_parameter_name, json_key=key)
    return config.json()

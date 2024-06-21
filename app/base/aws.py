import boto3
from typing import Dict
from app.config import settings


class AWSBaseService:
    service = None

    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self.service is None:
            raise NotImplementedError("service is not defined")

        if self._client is None:
            self._client = boto3.client(
                self.service,
                region_name=settings.aws_region,
                aws_access_key_id=settings.aws_access_key,
                aws_secret_access_key=settings.aws_secret_access_key
            )
        return self._client


class SSMParamStore:
    _instance = None
    _client = None
    _data: Dict = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SSMParamStore, cls).__new__(cls)
        return cls._instance

    def get_ssm_client(self):
        if self._client is None:
            self._client = boto3.client(
                "ssm",
                region_name=settings.aws_region,
                aws_access_key_id=settings.aws_access_key,
                aws_secret_access_key=settings.aws_secret_access_key
            )
        return self._client

    def fetch_params(self, path, recursive=False):
        ssm = self.get_ssm_client()
        next_token = None
        while True:
            if next_token:
                response = ssm.get_parameters_by_path(
                    Path=path,
                    Recursive=recursive,
                    WithDecryption=True,
                    NextToken=next_token,
                )
            else:
                response = ssm.get_parameters_by_path(
                    Path=path, Recursive=recursive, WithDecryption=True
                )
            params = response.get("Parameters")
            for param in params:
                self._data[param.get("Name")] = param.get("Value")
            next_token = response.get("NextToken")
            if not next_token:
                break

    def get_param_value(self, param):
        if param not in self._data:
            path = "/".join(param.split("/")[:-1])
            self.fetch_params(path)
        return self._data.get(param)

    def set_param_value(self, param, value, type):
        if param not in self._data:
            raise Exception("Invalid parameter")
        ssm = self.get_ssm_client()
        response = ssm.put_parameter(
            Name=param,
            Value=value,
            Type=type,
            Overwrite=True,
            Tier="Standard",
            DataType="text",
        )
        if not response.get("Version"):
            raise Exception(f"Failed to update parameter: {param}")
        self._data[param] = value

    def get_param_values(self, param):
        def param_exists(prefix, suffix):
            for key in self._data.keys():
                if key.startswith(prefix) and key.endswith(suffix):
                    return True
            return False

        """
        Split parameter into path, and parameter name

        param => /sandbox/bsestarmf/tarrakki/userid
        path => /sandbox/bsestarmf
        param_name => userid

        """
        path = "/".join(param.split("/")[:-1])
        param_name = param.split("/")[-1:][0]
        """
        Fetch parameters
        """
        if not param_exists(prefix=path, suffix=param_name):
            self.fetch_params(path=path, recursive=True)

        result = {}
        for key in self._data.keys():
            if key.startswith(path) and key.endswith(param_name):
                """
                Extract the key
                e.g., given /sandbox/bsestarmf/tarrakki/userid
                key => tarrakki
                """
                _key = key[len(path) + 1 : len(param_name) * -1 - 1]
                result[_key] = self._data[key]
        return result


class S3Service(AWSBaseService):
    service = "s3"

    def upload_file(self, file, bucket, key):
        self.client.upload_fileobj(file, bucket, key)

    def get_file(self, bucket, key):
        return self.client.get_object(Bucket=bucket, Key=key)["Body"].read()

    def delete_file(self, bucket, key):
        self.client.delete_object(Bucket=bucket, Key=key)

    def generate_presigned_url(self, bucket, key, expiration=3600):
        return self.client.generate_presigned_url(
            "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=expiration
        )


# def upload_document_to_s3(file, key):
#     s3 = S3Service()
#     s3.upload_file(file, settings.AWS_S3_BUCKET_NAME, key)


# def download_from_s3(key):
#     s3 = S3Service()
#     return s3.get_file(settings.AWS_S3_BUCKET_NAME, key)

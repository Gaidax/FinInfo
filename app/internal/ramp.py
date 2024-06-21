from app.internal.ApiCommons import ApiCommons
from app.config.ramp import config
#from app.db.DynamoDB import DynamoDB


class RampAPI(ApiCommons):
    """Class for RAMP API logic"""

    ApiBASE = config.base_url
    ApiCreateToken = config.create_token_api_endpoint
    ApiRampScreening = config.screening_api_endpoint

    username = config.username
    password = config.password
    clientId = config.client_id
    clientSecret = config.client_secret
    subBu = config.sub_business_unit
    token = config.token

    # Username = {"Axis": "AXIS123", "RBL": "RBL123"}
    TokenHeaders = {
        "username": username,
        "password": password,
        "clientId": clientId,
        "clientSecret": clientSecret,
        "Content-Type": "text/plain",
        "subBu": subBu,
    }

    @classmethod
    def create_request_headers(cls, payload=...):
        result = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {cls.token}",
        }
        return result

    @classmethod
    async def token_creation_method(cls):
        token = await cls.make_async_request(
            "POST", cls.ApiCreateToken, custom_headers=cls.TokenHeaders
        )
        # config["RampAPI"]["api.ramp.token"] = token["token"]
        # with open(conf_file, "w") as configfile:
        #     config.write(configfile)
        config.token = token["token"]
        cls.token = token["token"]

    @classmethod
    async def ramp_screening(cls,requestPayload: dict):
        """
        Class method that makes async request to RAMP API ApiRampScreening

        :param requestPayload: incoming json payload for the RAMP API, model class RampScreeningRequestModel
        :return: Response JSON payload with screening match information
        """
        #dynamo = DynamoDB()
        #key = requestPayload['rampRequest']['listMatchingPayload']['requestListVO']['pan']
        #existing_entry = dynamo.ScreeningTable.get_item(Key={"pan": key})
        #entries = existing_entry.get('Item')
        #if entries:
        #    return entries['results']
        screening_response = await cls.make_async_request(
            "POST",cls.ApiRampScreening,payload=requestPayload
        )
        #api_results = {'results':screening_response['rampResponse']['listMatchResponse']['matchResult']['responseVOList']}
        #api_results['pan']=key
        #dynamo.ScreeningTable.put_item(Item=api_results)
        return screening_response#api_results['results']
    
    @classmethod
    async def rampScreening401(cls, requestPayload: dict):
        """Class method to test 401 bad token flow"""
        return await cls.make_async_request("POST", "401_test", payload=requestPayload)

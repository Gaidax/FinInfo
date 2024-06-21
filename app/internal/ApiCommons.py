from abc import abstractmethod
import random
import aiohttp
from sqlalchemy.orm import Session
from app.utils import SSL_CONTEXT,asyncio,config
from app.repository.session import get_session_data_list

class AuthException(Exception):
    def __init__(self, message = "AUTH ERROR OCCURED"):
        self.message = message

    def __str__(self):
        return self.message

class TooManyRequestsException(Exception):
    def __init__(self, message = "TOO MANY REQUESTS ERROR OCCURED"):
        self.message = message

    def __str__(self):
        return self.message

class ApiCommons:
    """Class for Common API logic"""
    ApiBASE = ''
    RetriesCount = int(config['AppConfig']['retries_count'])
    Timeout = int(config['AppConfig']['read_timeout_value'])
    ConnectTimeout = int(config['AppConfig']['connect_timeout_value'])
    
    @classmethod
    def request_method(cls,session,action):
        """
        Class method that makes async request to this API

        :param action: string for http method GET, POST, DELETE, PUT etc.
        :param session: aiohttp session object
        :return: aiohttp session rest http method 
        """
        match action:
            case "GET":
                return session.get
            case "POST":
                return session.post
            case "PUT":
                return session.put
            case _:
                return session.get
        

    @classmethod
    @abstractmethod
    async def token_creation_method(cls):
        """
        Abstract class method that is used by derived classes to create Auth tokens
        
        :return: None
        """
        return
    
    @classmethod
    @abstractmethod
    def create_request_headers(cls,payload=dict()):
        """
        Abstract class method that is used by derived classes to create Auth headers

        :param payload: payload may be needed in the header for signing
        :return: None
        """
        return
    
    @classmethod
    def check_session_data(
        cls, db: Session, session_id: str, _tag:str
    ):
        session_data_list = get_session_data_list(
        db=db, session_id=session_id, tag=_tag
        )
        if len(session_data_list) == 1:
            return session_data_list[0].data
        else:
            return None

    @classmethod
    async def make_async_request(cls,method,url,payload={},custom_headers={},retries=0):
        """
        Class method that makes async request to this API

        :param method: Aiohttp client method GET, POST, DELETE, PUT etc. defined in class method request_method
        :param url: API endpoint
        :param retries: internal retry counter
        :param payload: JSON payload for REST calls that require payload
        :param custom_headers: headers for requests with atypical headers for the API (like token creation requests)
        :return: Response JSON
        """
        try:
            async with aiohttp.ClientSession(headers=cls.create_request_headers(payload) if not custom_headers else custom_headers, \
                                             timeout = aiohttp.ClientTimeout(total=cls.Timeout)) as session:#total in ClientTimeout is a timeout for the whole request connection + read;use sock_read and sock_connect for separation
                async with cls.request_method(session,method)(cls.ApiBASE+url, ssl=SSL_CONTEXT) if not payload else \
                        cls.request_method(session,method)(cls.ApiBASE+url,json=payload, ssl=SSL_CONTEXT) as api_response:
                    
                    if api_response.status == 401:#TODO: generalize bad token responses vkyc & ramp
                        raise AuthException()
                    elif api_response.status in [443]:#TODO: throtling for external API calls - error 
                        raise TooManyRequestsException()
                    else:
                        if api_response.content_type == "application/json":
                            return await api_response.json()#if not any of those cases error is not expected
                        api_response.raise_for_status()
                        return await api_response.text()
                        
                    
        except TooManyRequestsException as e:
            if retries < cls.RetriesCount:
                retries+=1
                await asyncio.sleep(random.randint(1,10))
                return await cls.make_async_request(method,url,payload,custom_headers,retries)
            else:
                return {"error":e.message}     

        except AuthException as e:
            if retries < cls.RetriesCount:
                await cls.token_creation_method()
                retries+=1
                return await cls.make_async_request(method,url,payload,custom_headers,retries)
            else:
                return {"error":e.message}  
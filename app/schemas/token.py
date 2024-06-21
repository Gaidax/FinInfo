from pydantic import BaseModel

class CreateTokenRequestSchema(BaseModel):
    username:str
    password:str
    clientId:str
    clientSecret:str
    subBu:str

class CreateTokenResponseSchema(BaseModel):
    token: str

class GenerateTokenRequestSchema(BaseModel):
    username: str
    password: str

class GenerateTokenResponseSchema(BaseModel):
    Token: str
    status_code: int
    success: bool
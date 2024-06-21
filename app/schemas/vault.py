from pydantic import BaseModel
from typing import List


class BaseRequestSchema(BaseModel):
    refData: str
    refDataType: str


class BaseResponseSchema(BaseModel):
    action: str
    response_code: int
    response_message: str
    total_size: int
    total_pages: int


class InsertApiRequestSchema(BaseRequestSchema):
    pass


class InsertApiResponseSchema(BaseResponseSchema):
    results: List[str]


class ResultSchema(BaseModel):
    id: int
    refId: str
    refData: str
    refDataType: str
    tokenId: str | None
    isActive: int


class GetByRefIdApiResponseSchema(BaseResponseSchema):
    results: List[ResultSchema]


class GetByRefDataApiRequestSchema(BaseRequestSchema):
    pass


class GetByRefDataApiResponseSchema(BaseResponseSchema):
    results: List[ResultSchema]

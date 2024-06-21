from typing import List, Optional
from pydantic import BaseModel, Field


class RequestVoSchema(BaseModel):
    aadhar: Optional[str] = ""
    address: Optional[str] = ""
    city: Optional[str] = ""
    concatAddress: Optional[str] = ""
    country: Optional[str] = ""
    customerId: Optional[str] = ""
    digitalID: Optional[str] = ""
    din: Optional[str] = ""
    dob: Optional[str] = ""
    docNumber: Optional[str] = ""
    drivingLicence: Optional[str] = ""
    email: Optional[str] = ""
    entityName: Optional[str] = ""
    name: Optional[str] = ""
    nationality: Optional[str] = ""
    pan: Optional[str] = ""
    passport: Optional[str] = ""
    phone: Optional[str] = ""
    pincode: Optional[str] = ""
    rationCardNo: Optional[str] = ""
    ssn: Optional[str] = ""
    state: Optional[str] = ""
    tin: Optional[str] = ""
    voterId: Optional[str] = ""


class RequestListVoSchema(BaseModel):
    businessUnit: str
    requestType: str
    requestVOList: List[RequestVoSchema]
    subBusinessUnit: str


class requestListVo(BaseModel):
    requestListVO: RequestListVoSchema


class listMatchingPayload(BaseModel):
    listMatchingPayload: requestListVo


class RampScreeningRequestSchema(BaseModel):
    rampRequest: listMatchingPayload


class Fields(BaseModel):
    matchedField: str
    sourceData: str
    targetData: str


class TargetData(BaseModel):
    Address: str
    AliasName: str
    CBICIRCULARNO: str
    City: str
    Country: str
    Customer_Address_1: str = Field(allias="Customer Address 1")
    CustomerID: int
    DOBText: str
    Location: str
    Name: str
    OriginalSource: str
    PAN: str
    Passport: str
    POB: str
    RBICIRCULARNO: str
    Source: str


class responseVOList(BaseModel):
    entryId: int
    fields: List[Fields]
    listName: str
    primaryName: str
    score: str
    targetData: TargetData


class matchResult(BaseModel):
    matchFlag: bool
    responseVOList: List[responseVOList]
    searchedDate: str
    searchedFor: str


class listMatchResponse(BaseModel):
    matchResult: matchResult
    responseHash: str
    salt: str


class RampScreeningResponseSchema(BaseModel):
    rampResponse: listMatchResponse
    statusCode: str
    statusMessage: str
    txnId: int

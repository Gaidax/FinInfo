from pydantic import BaseModel 


class RiskParameter(BaseModel):
    annualIncomeTurnOver: str
    correspondAddrCountry: str
    countryOfIncorporation: str
    custCategory: str
    industry: str
    nationality: str
    occupation: str
    pep: str
    prodSubType: str

class RiskRatingCalculationAPIRequest(BaseModel):
    isEntity: str = "0"
    requestId: str
    riskParameter: RiskParameter


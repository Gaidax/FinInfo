from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator, Field


class VerifyPanRequestSchema(BaseModel):
    """
    TODO: validate input
    1. pan matches pattern ABCDE1234X
    2. name contains alphabets space
    3. dob should not be future, age should be 18+
    4. done - consent is true
    """

    pan: str = Field(pattern=r"^([^A-Z]*[A-Z]){5}([0-9]){4}([A-Z]){1}")
    name: str = Field(pattern=r"^[a-zA-Z ]*$")
    father_name: str = Field(pattern=r"^[a-zA-Z ]*$")
    dob: datetime
    consent: bool

    @field_validator("dob")
    @classmethod
    def validate_date_of_birth(cls, value: datetime):
        now_ts = datetime.now().timestamp()
        val_ts = value.timestamp()
        if val_ts > now_ts:
            raise ValueError("Date is in future")
        if now_ts - val_ts < 568024668:  # evaluate offset awarness
            raise ValueError("Less than 18 years of age")

        return value

    @field_validator("consent")
    @classmethod
    def validate_consent(cls, value: bool):
        if value is not True:
            raise ValueError("Consent denied.")

        return value


class GetCustomerIdRequestSchema(BaseModel):
    aadharCard: Optional[str] = None
    panCard: Optional[str] = None


class ProteanPanVerificationRecordSchema(BaseModel):
    pan: str
    pan_status: str
    name: str
    fathername: str
    dob: str
    seeding_status: str

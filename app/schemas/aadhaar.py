from pydantic import BaseModel, field_validator


class AadhaarOtpRequestSchema(BaseModel):
    aadhaar_number: str
    consent: bool

    # TODO: input validations
    # 1. Aadhaar pattern match
    # 2. mobile

    @field_validator("consent")
    @classmethod
    def validate_consent(cls, value: bool):
        if value is not True:
            raise ValueError("Consent denied.")

        return value


class AadhaarVerifyOtpRequestSchema(BaseModel):
    otp: str
    aadhaar_number: str
    consent: bool

    # TODO: input validations
    # 1. Aadhaar pattern match
    # 2. consent must be true

    @field_validator("consent")
    @classmethod
    def validate_consent(cls, value: bool):
        if value is not True:
            raise ValueError("Consent denied.")

        return value

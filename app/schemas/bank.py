from pydantic import BaseModel, model_validator


class CreateBankAccountRequestSchema(BaseModel):
    account_number: str
    ifsc: str

    @model_validator(mode="before")
    def validate_input(cls, values):
        """
        TODO: validate input
        1. bank account number matches pattern
        2. ifsc matches pattern
        """
        return values

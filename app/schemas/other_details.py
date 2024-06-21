from enum import Enum
from pydantic import BaseModel


class OccupationEnum(str, Enum):
    business = "business"
    agriculture = "agriculture"
    forex_dealer = "forex_dealer"
    service_public_sector = "service_public_sector"
    service_private_sector = "service_private_sector"
    service_government_sector = "service_government_sector"
    others_professional = "others_professional"
    others_self_employed = "others_self_employed"
    others_retired = "others_retired"
    others_housewife = "others_housewife"
    others_student = "others_student"
    others = "others"


class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    transgender = "transgender"


class EducationEnum(str, Enum):
    under_graduate = "under_graduate"
    graduate = "graduate"
    post_graduate = "post_graduate"


class MaritialStatusEnum(str, Enum):
    married = "married"
    unmarried = "unmarried"
    other = "other"


class AnnualIncomeEnum(str, Enum):
    upto_5_lakh = "upto_5_lakh"
    above_5_lakh_upto_10_lakh = "above_5_lakh_upto_10_lakh"
    above_10_lakh_upto_25_lakh = "above_10_lakh_upto_25_lakh"
    above_25_lakh_upto_50_lakh = "above_25_lakh_upto_50_lakh"
    above_50_lakh_upto_1_crore = "above_50_lakh_upto_1_crore"
    above_1_crore = "above_1_crore"


class OtherDetailRequestSchema(BaseModel):
    occupation: OccupationEnum
    education: EducationEnum
    marital_status: MaritialStatusEnum
    gender: GenderEnum
    annual_income: AnnualIncomeEnum
    non_pep_declaration: bool
    fatca_declaration: bool

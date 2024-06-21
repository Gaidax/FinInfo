from enum import Enum
from pydantic import BaseModel
from typing import List


class AgeGroupEnum(int, Enum):
    MINOR = 1
    SENIOR_CITIZEN = 2
    SUPER_SENIOR_CITIZEN = 3
    REGULAR = 4


class customerInformationSchema(BaseModel):
    aadharNoStr: str
    ageGroupInt: int
    annualIncomeCategoryCodeLon: int  # Picklist 78
    ckycrNoStr: str = "N/A"
    countryOfResidenceLon: int  # Picklist 90
    customerGroupIdLon: int = -1
    customerIcStr: str = "-1"
    customerIdLon: int = -1
    customerOpenDateDtm: str
    customerProfileCodeInt: int  # Picklist 104
    customerSubTypeCodeInt: int  # Picklist 95
    customeTypeCodeLon: int = 1
    dateOfBirthDtm: str
    defaultAccountNoLon: int = -1
    educationCodeLon: int  # Picklsit 77
    employeeIdStr: str = "N/A"
    FatherSalutationStr: str  # Picklist 116
    FatherFirstNameStr: str
    FatherMiddleNameStr: str
    firstNameStr: str
    middleNameStr: str
    lastNameStr: str
    form60FlagInt: int = -1  # 1 if pan not available, -1 otherwise
    form60ReasonInt: int = -1  # Pick list 100
    fullNameStr: str
    guardianTypeCodeLon: int = -1
    homeBranchCodeLon: int
    introducersIdLon: int  # Picklist 303
    maritalStatusCodeLon: int  # Picklist 27
    MotherSalutationStr: str  # Picklist 116
    MotherFirstNameStr: str
    MotherMiddleNameStr: str
    MotherLastNameStr: str
    nationalityCodeLon: int  # Picklist 50
    panNoStr: str
    placeOfBirthStr: str = "N/A"
    registeredMobileNoStr: str
    relationshipOfficerIdStr: str = "N/A"
    religionCodeLon: str  # Picklist 91
    riskRatingInt: int  # Picklist 103
    salutationStr: str  # Picklist 116
    sexCodeLon: int  # Picklist 24
    shortNameStr: str = "N/A"
    SpouseFirstNameStr: str = "N/A"
    SpouseLastNameStr: str = "N/A"
    SpouseMiddleNameStr: str = "N/A"
    SpouseSalutationStr: str = -1  # Picklist 116
    staffFlagInt: int = -1
    statusCodeLon: int  # Picklist 47


class AddressTypeEnum(int, Enum):
    PERMANENT = 1
    CORRESPONDANCE = 2


class AddressSchema(BaseModel):
    address1Str: str
    address2Str: str
    address3Str: str
    addressTypeCodeLon: int
    boardLineNoStr: str = "N/A"
    cityCodeLon: int  # Picklist 3
    countryCodeLon: int  # Picklist 90
    customerIdLon: int = -1
    emailIdStr: str = "N/A"
    extensionNoStr: str = "N/A"
    faxNoStr: str = "N/A"
    mobileNoStr: str = "N/A"
    phoneOffStr: str = "N/A"
    phoneResStr: str = "N/A"
    pinCodeLon: int
    stateCodeLon: int  # Picklist 4
    stdFaxNoStr: str = "N/A"
    stdOffStr: str = "N/A"
    stdResStr: str = "N/A"


class InsertAuthorizeCustomerRequestSchema(BaseModel):
    customerInformation: customerInformationSchema
    mailingAddress: AddressSchema
    permanentAddress: AddressSchema


class InsertAuthorizeCustomerResponseSchema(BaseModel):
    action: str
    response_code: int
    response_message: str
    results: List[str]
    total_pages: int
    total_size: int

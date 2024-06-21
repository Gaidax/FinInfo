from pydantic import BaseModel, StrictInt, Field

class customerInformation(BaseModel):
    aadharNoStr: str
    ageGroupInt: int
    annualIncomeCategoryCodeLon: StrictInt = Field(..., format='int64')
    ckycrNoStr: str
    countryOfResidenceLon: StrictInt = Field(..., format='int64')
    customerGroupIdLon: StrictInt = Field(..., format='int64')
    customerIcStr:    str
    customerIdLon: StrictInt = Field(..., format='int64')
    customerOpenDateDtm: str
    customerProfileCodeInt: int
    customerSubTypeCodeInt: int
    customeTypeCodeLon: StrictInt = Field(..., format='int64')
    dateOfBirthDtm: str
    defaultAccountNoLon: StrictInt = Field(..., format='int64')
    educationCodeLon: StrictInt = Field(..., format='int64')
    employeeIdStr: str
    FatherFirstNameStr: str
    FatherMiddleNameStr: str
    FatherSalutationStr: str
    firstNameStr: str
    form60FlagInt: int
    form60ReasonInt: int
    fullNameStr: str
    guardianTypeCodeLon: StrictInt = Field(..., format='int64')
    homeBranchCodeLon: StrictInt = Field(..., format='int64')
    introducersIdLon: StrictInt = Field(..., format='int64')
    lastNameStr: str
    maritalStatusCodeLon: StrictInt = Field(..., format='int64')
    middleNameStr: str
    MotherFirstNameStr: str
    MotherLastNameStr: str
    MotherMiddleNameStr: str
    MotherSalutationStr: str
    nationalityCodeLon: StrictInt = Field(..., format='int64')
    panNoStr: str
    placeOfBirthStr: str
    registeredMobileNoStr: str
    relationshipOfficerIdStr: str
    religionCodeLon: StrictInt = Field(..., format='int64')
    riskRatingInt: int
    salutationStr:str
    sexCodeLon: StrictInt = Field(..., format='int64')
    shortNameStr: str
    SpouseFirstNameStr: str
    SpouseLastNameStr: str
    SpouseMiddleNameStr: str
    SpouseSalutationStr: str
    staffFlagInt: int
    statusCodeLon: StrictInt = Field(..., format='int64')


class mailingAddress(BaseModel):
    ddress1Str: str
    address2Str: str
    address3Str: str
    addressTypeCodeLon: StrictInt = Field(..., format='int64')
    boardLineNoStr: str
    cityCodeLon: StrictInt = Field(..., format='int64')
    countryCodeLon: StrictInt = Field(..., format='int64')
    customerIdLon: StrictInt = Field(..., format='int64')
    emailIdStr: str
    extensionNoStr: str
    faxNoStr: str
    mobileNoStr: str
    phoneOffStr: str
    phoneResStr: str
    pinCodeLon: StrictInt = Field(..., format='int64')
    stateCodeLon: StrictInt = Field(..., format='int64')
    stdFaxNoStr: str
    stdOffStr: str
    stdResStr: str

class permanentAddress(BaseModel):
    ddress1Str: str
    address2Str: str
    address3Str: str
    addressTypeCodeLon: StrictInt = Field(..., format='int64')
    boardLineNoStr: str
    cityCodeLon: StrictInt = Field(..., format='int64')
    countryCodeLon: StrictInt = Field(..., format='int64')
    customerIdLon: StrictInt = Field(..., format='int64')
    emailIdStr: str
    extensionNoStr: str
    faxNoStr: str
    mobileNoStr: str
    phoneOffStr: str
    phoneResStr: str
    pinCodeLon: StrictInt = Field(..., format='int64')
    stateCodeLon: StrictInt = Field(..., format='int64')
    stdFaxNoStr: str
    stdOffStr: str
    stdResStr: str

class CustomerOnboardingRequest(BaseModel):
    customerInformation:customerInformation
    mailingAddress:mailingAddress
    permanentAddress:permanentAddress
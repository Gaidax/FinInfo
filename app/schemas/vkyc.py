from pydantic import BaseModel

class PersonalInformation(BaseModel):
    aadhaar_address: str
    current_address_address_line_1: str
    current_address_address_line_2: str
    current_address_address_line_3: str
    current_address_city: str
    current_address_not_same_as_aadhaar_address: bool
    current_address_pincode: str
    current_address_state: str
    dob: str
    gender: str
    name: str

class PersonalDetails(BaseModel):
    education: str
    father_spouse_full_name: str
    gross_annual_income: str
    marital_status: str
    mother_name: str
    occupation: str
    source_of_income: str

class NomineeDetails(BaseModel):
    nominee_address: str
    nominee_address_same_as_current_address: bool
    nominee_date_of_birth: str
    nominee_full_name: str
    provide_nominee_details: str
    relationship_with_nominee: str

class EkycDetails(BaseModel):
    aadhaarNo: str
    address:str
    careOf: str
    city: str
    district: str
    location: str
    name: str
    photo: str
    pin: str
    state: str
    subdistrict: str
    ekyc_timestamp: str

class VerifyAadhaarOtp(BaseModel):
    ekycDetails: EkycDetails

class AmlCheck(BaseModel):
    aml_exists: bool

class BasicDetails(BaseModel):
    email: str
    pan_number: str
    politically_exposed_consent: bool
    AML_CHECK: AmlCheck
    VERIFY_AADHAAR_OTP: VerifyAadhaarOtp


class Data(BaseModel):
    BASIC_DETAILS: BasicDetails
    NOMINEE_DETAILS: NomineeDetails
    PERSONAL_DETAILS: PersonalDetails
    PERSONAL_INFORMATION: PersonalInformation

class Stage1Data(BaseModel):
    Data: Data

class Extras(BaseModel):
    product_code: str
    stage_1_data: Stage1Data

class VkycSendLinkRequest(BaseModel):
    link_type:str
    user_id: str
    phone_number: str
    session_type: str
    send_notification: str
    extras: Extras

class VkycSendLinkResponse(BaseModel):
    link_expiry_time: str
    link_id: str
    link_url: str
    phone_number: str
    session_id: str
    user_id: str
    validity_duration: int


class SessionData(BaseModel):
    agent_assignment_time: str
    client_name: str
    end_time: str
    extras:str
    link_id: str
    phone_number: str
    productCode: str
    session_id: str
    session_status: str
    session_type: str
    start_time: str
    user_id: str

class GetDetailsResponse(BaseModel):
    session_data:SessionData
    status: int
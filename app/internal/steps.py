from uuid import uuid4
from sqlalchemy.orm import Session
from app.schemas.pan import VerifyPanRequestSchema, ProteanPanVerificationRecordSchema
from app.schemas.aadhaar import AadhaarOtpRequestSchema
from app.schemas.common import StepStatus, StepType
from app.schemas.other_details import OtherDetailRequestSchema
from app.repository.pan import get_pan_status, get_status_remark
from app.repository.session import (
    get_session_data_list,
    create_session_data,
    create_session_state,
    update_session_data,
    update_session_state,
    get_session_state_list,
)
from app.internal.protean import ProteanAPI

from typing import Tuple
from app.internal.turing import TuringAPI
from app.internal.ramp import RampAPI
from app.schemas.ramp import RampScreeningRequestSchema
from app.config.ramp import config
from app.utils import rootLogger as logger
from app.internal.karza import KarzaApi
from app.models import SessionDataModel

TAG_PAN_VERIFICTION_REQUEST = "pan.verify.request"
TAG_PAN_VERIFICATION_PROTEAN_RESPONSE = "pan.verify.protean.response"
TAG_EAADHAAR_VERIFICTION_REQUEST = "eaadhaar.verify.request"
TAG_EAADHAAR_VERIFICATION_SEND_OTP_RESPONSE = "eaadhaar.sendotp.karza.response"
TAG_OTHER_DETAILS = "other_details"


async def is_existing_customer(pan: str) -> bool:
    customer_record = await TuringAPI.get_customer_id_by_pan_aadhar(pan_card=pan)
    if customer_record:
        return True
    return False


async def is_aml_match(pan: str) -> bool:
    data = {
        "rampRequest": {
            "listMatchingPayload": {
                "requestListVO": {
                    "businessUnit": config.business_unit,
                    "requestType": config.request_type,
                    "requestVOList": [
                        {
                            "pan": pan,
                        }
                    ],
                    "subBusinessUnit": config.sub_business_unit,
                }
            }
        }
    }
    schema = RampScreeningRequestSchema(**data)
    payload = schema.model_dump()
    result = await RampAPI.ramp_screening(payload)
    return result["rampResponse"]["listMatchResponse"]["matchResult"]["matchFlag"]


async def get_pan_verification_status(
    db: Session, session_id: str, input: VerifyPanRequestSchema
) -> Tuple:
    session_data = get_session_data_list(
        db=db, session_id=session_id, tag=TAG_PAN_VERIFICATION_PROTEAN_RESPONSE
    )
    if session_data is not None:
        pan_record = ProteanPanVerificationRecordSchema.model_validate_json(
            session_data[0].data
        )
    elif session_data is None:
        # pan_record = await ProteanAPI.verifyPan_v2(input=input)
        pan_record = await ProteanAPI.verifyPan(input=input)
        create_session_data(
            db=db,
            session_id=session_id,
            tag=TAG_PAN_VERIFICTION_REQUEST,
            data=input.model_dump_json(),
        )
        create_session_data(
            db=db,
            session_id=session_id,
            tag=TAG_PAN_VERIFICATION_PROTEAN_RESPONSE,
            data=input.model_dump_json(),
        )

    # return
    pan_status = get_pan_status(pan_record)
    if pan_status == StepStatus.success:
        return pan_status, None
    return pan_status, get_status_remark(pan_record)


async def do_pan_verification(
    db: Session, session_id: str, input: VerifyPanRequestSchema
) -> Tuple:
    try:
        # Verify PAN - NSDL/Protean
        status, status_remark = await get_pan_verification_status(
            db=db, session_id=session_id, input=input
        )
        if status == StepStatus.failed:
            return status, status_remark

        # existing customer?
        if await is_existing_customer(pan=input.pan) is True:
            return StepStatus.failed, "Account already exists"

        # AML check
        if await is_aml_match(pan=input.pan) is True:
            return StepStatus.failed, "Please contact branch office"

        return StepStatus.success, None
    except Exception as e:
        logger.exception(e)
        return (
            StepStatus.error,
            "Unable to process your request, please try after some time",
        )


async def do_send_otp(db: Session, session_id: str, input: AadhaarOtpRequestSchema):
    max_attempt = 3
    attempt_count = 0
    session_data = get_session_data_list(
        db=db, session_id=session_id, tag=TAG_EAADHAAR_VERIFICATION_SEND_OTP_RESPONSE
    )
    if session_data is not None:
        max_attempt = 3
        attempt_count = len(session_data)
        if attempt_count >= max_attempt:
            return {
                "id": uuid4().hex,
                "type": StepType.eaadhaar,
                "status": StepStatus.failed,
                "status_remark": "Max attempt exceeded",
                "attempt_boundary": 3600,
                "attempt_gap": 30,
                "max_attempt": max_attempt,
                "attempt_count": attempt_count,
            }

    # make an attempt
    case_id = uuid4().hex
    response = await KarzaApi.sendOtp(
        payload={
            "aadhaarNo": input.aadhaar_number,
            "consent": "Y" if input.consent is True else "N",
            "clientData": {"caseId": case_id},
        }
    )
    create_session_data(
        db=db,
        session_id=session_id,
        tag=TAG_EAADHAAR_VERIFICTION_REQUEST,
        data=input.model_dump_json(),
    )
    create_session_data(
        db=db,
        session_id=session_id,
        tag=TAG_EAADHAAR_VERIFICATION_SEND_OTP_RESPONSE,
        data=response,
    )
    # increment attempt
    attempt_count += 1

    if response["status"] == 101:
        return {
            "id": uuid4().hex,
            "type": StepType.eaadhaar,
            "status": StepStatus.success,
            "status_remark": None,
            "attempt_boundary": 3600,
            "attempt_gap": 30,
            "max_attempt": max_attempt,
            "attempt_count": attempt_count,
        }

    # dummy response
    if input.aadhaar_number == "123456781234":
        return {
            "id": uuid4().hex,
            "type": StepType.eaadhaar,
            "status": StepStatus.in_progress,
            "status_remark": "",
            "attempt_boundary": 3600,
            "attempt_gap": 30,
            "max_attempt": max_attempt,
            "attempt_count": attempt_count,
        }

    return {
        "id": uuid4(),
        "type": StepType.eaadhaar,
        "status": StepStatus.failed,
        "status_remark": "Mobile number not linked",
        "attempt_boundary": 3600,
        "attempt_gap": 30,
        "max_attempt": max_attempt,
        "attempt_count": attempt_count,
    }


async def create_other_details(
    db: Session, session_id: str, input: OtherDetailRequestSchema
) -> Tuple:
    session_data = create_session_data(
        db=db,
        session_id=session_id,
        tag=TAG_OTHER_DETAILS,
        data=input.model_dump(),
    )
    session_state = create_session_state(
        db=db,
        session_id=session_id,
        step=StepType.other_detail,
        status=StepStatus.success,
    )
    return (session_data, session_state)


async def update_other_details(
    db: Session,
    session_id: str,
    session_data: SessionDataModel,
    input: OtherDetailRequestSchema,
) -> Tuple:
    session_data = update_session_data(
        db=db,
        session_data=session_data,
        data=input.model_dump(),
    )
    session_state_list = get_session_state_list(
        db=db, session_id=session_id, step=StepType.other_detail
    )
    session_state = None
    if len(session_state_list) == 0:
        session_state = create_session_state(
            db=db,
            session_id=session_id,
            step=StepType.other_detail,
            status=StepStatus.success,
        )
    elif len(session_state_list) == 1:
        session_state = update_session_state(
            db=db, session_state=session_state_list[0], status=StepStatus.success
        )
    return (session_data, session_state)
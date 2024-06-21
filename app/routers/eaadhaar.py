from uuid import uuid4
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.aadhaar import AadhaarOtpRequestSchema, AadhaarVerifyOtpRequestSchema
from app.schemas.common import StepType, StepStatus
from app.internal.karza import KarzaApi
from app.internal.steps import do_send_otp
from app.utils import rootLogger as logger


router = APIRouter(prefix="/eaadhaar", tags=["eaadhaar"])


@router.post("/send-otp")
async def send_otp(
    request: Request, input: AadhaarOtpRequestSchema, db: Session = Depends(get_db)
):
    """
    - Validate inputs - pydantic
    - Rate limit - use aadhaar as key
    - Validate session
    - Verify whether the step is already complete
    ***
    custom rate limit: send/resend limit per window, per session
    ***
    - invoke API (send otp)
      - success: next step
      - fail: return

    Dependencies:
    - Aadhaar API - not available
    """

    return await do_send_otp(db=db, session_id=request.state.session_id, input=input)


@router.post("/verify-otp")
async def verify_otp(request: Request, input: AadhaarVerifyOtpRequestSchema):
    """
    - Validate inputs - pydantic
    - Validate session
    - Verify whether the step is already complete
    - Limit attempts, block user for n minutes after m attempts
    - invoke API (verify otp)
      - success: next step
      - fail: return

    Dependencies:
    - DEMO AUTH - to check whether mobile is linked with aadhaar
    - Aadhaar API - not available (XML validation)
    - dedupe check - available
    - jocata - AML, Risk Rating - available


    Response: in case of verification failure, inform about remaining attempts.
    """

    case_id = uuid4().hex
    response = await KarzaApi.VerifyOtp(
        payload={
            "otp": input.otp,
            "accessKey": "eb81bf52-ddb7-4802-a031-0982b6aba9cb",
            "aadhaarNo": input.aadhaar_number,
            "shareCode": "5555",
            "consent": "Y" if input.consent is True else "N",
            "clientData": {"caseId": case_id},
        }
    )
    logger.info(response)

    session_id = request.state.session_id

    # dummy response
    if input.otp == "123456":
        raise HTTPException(status_code=400, detail={"message": "OTP has expired"})

    if input.aadhaar_number == "123456781234":
        return {
            "id": session_id,
            "type": StepType.eaadhaar,
            "status": StepStatus.success,
            "status_remark": None,
        }

    return {
        "id": session_id,
        "type": StepType.eaadhaar,
        "status": StepStatus.in_progress,
        "status_remark": "Invalid OTP",
    }

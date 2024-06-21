from fastapi import Request, APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.pan import VerifyPanRequestSchema
from app.schemas.common import StepType
from app.internal.steps import do_pan_verification
from app.repository.session import get_session_state_list
from app.database import get_db

router = APIRouter(prefix="", tags=["pan"])


@router.post("/verify-pan")
async def verify_pan(
    request: Request, input: VerifyPanRequestSchema, db: Session = Depends(get_db)
):
    """
    - Validate inputs - pydantic
    - Validate session
    - Verify whether the step is already complete
    - invoke Protean PAN verification API - check whether aadhaar is linked.
            - success: next step
            - fail: return
    - invoke dedupe API - check whether the customer is new customer.
            - success: next step
            - fail: return
    - invoke AML check API
            - success: next step
            - fail: return
    - update session
    - return
    - error handling

    Dependencies:
    - Protean - PAN - available
    - 10. Get Customer ID - Aadhaar / PAN
    3. AML - ?
    """

    session_id = request.state.session_id
    session_data = get_session_state_list(db=db, session_id=session_id, step=StepType.pan)
    if session_data:
        return

    status, status_remark = await do_pan_verification(
        db=db, session_id=session_id, input=input
    )

    return {
        "id": request.state.session_id,
        "type": StepType.pan,
        "status": status,
        "status_remark": status_remark,
    }

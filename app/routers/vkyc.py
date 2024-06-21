from fastapi import Request, APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.common import StepType
from app.internal.vkyc import VkycAPI
from app.repository.session import get_session_state_list
from app.database import get_db

router = APIRouter(prefix="/vkyc", tags=["vkyc"])


@router.post("create_link")
async def create_link(
    request: Request,
    #input:VkycSendLinkRequest,
    db: Session = Depends(get_db)
    ):
    """
    Create link endpoint. Creates a link via VKYC API and stores it in the session

    :param db: db session
    :param request: Request object, has a state with session id
    :return: Json with step details
    """
    session_id = request.state.session_id
    session_data = get_session_state_list(db=db, session_id=session_id, step=StepType.vkyc)
    if session_data:
        return
    status, status_remark = await VkycAPI.vkyc_send_link(
        db=db, session_id=session_id
    )
    return {
        "id": session_id,
        "type": StepType.vkyc,
        "status": status,
        "status_remark": status_remark,
    }


@router.get("get_user_details/{session_id}")
async def get_user_details(
    #request: Request,
    session_id:str,
    db: Session = Depends(get_db)
    ):
    """
    Get user details. Gets user details via VKYC API and stores it in the session

    :param db: db session
    :param session_id: session_id incoming in url param like described in unity/issues/6
    :return: Json with step details
    """
    #session_id = request.state.session_id
    status, status_remark = await VkycAPI.get_details(
        db=db, session_id=session_id
    )
    return {
        "id": session_id,
        "type": StepType.vkyc,
        "status": status,
        "status_remark": status_remark,
    }

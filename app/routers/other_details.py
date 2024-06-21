from sqlalchemy.orm import Session
from fastapi import APIRouter, Request, Depends, HTTPException
from app.database import get_db
from app.schemas.other_details import OtherDetailRequestSchema
from app.internal.steps import (
    create_other_details,
    TAG_OTHER_DETAILS,
    update_other_details,
)
from app.repository.session import get_session_data_list

router = APIRouter(prefix="/other-details", tags=["other-details"])


@router.post("")
async def create(
    request: Request, input: OtherDetailRequestSchema, db: Session = Depends(get_db)
):
    session_id = request.state.session_id
    session_data_list = get_session_data_list(
        db=db, session_id=session_id, tag=TAG_OTHER_DETAILS
    )
    if len(session_data_list) > 0:
        raise HTTPException(
            status_code=409, detail={"message": "Session data already exist"}
        )
    _, session_state = create_other_details(
        db=db, session_id=request.state.session_id, input=input
    )
    return {
        "id": session_id,
        "type": session_state.state,
        "status": session_state.status,
        "status_remark": None,
    }


@router.get("")
async def get(request: Request, db: Session = Depends(get_db)):
    session_id = request.state.session_id
    session_data_list = get_session_data_list(
        db=db, session_id=session_id, tag=TAG_OTHER_DETAILS
    )
    if len(session_data_list) == 1:
        return session_data_list[0].data
    return {"message": "Session data not available"}


@router.put("")
async def put(
    request: Request, input: OtherDetailRequestSchema, db: Session = Depends(get_db)
):
    session_id = request.state.session_id
    session_data_list = get_session_data_list(
        db=db, session_id=session_id, tag=TAG_OTHER_DETAILS
    )
    if len(session_data_list) == 0:
        raise HTTPException(
            status_code=409, detail={"message": "Session data does not exist"}
        )
    if len(session_data_list) > 1:
        raise Exception("More than 1 instances found for session data")

    _, session_state = await update_other_details(
        db=db,
        session_data=session_data_list[0],
        session_id=request.state.session_id,
        input=input,
    )
    return {
        "id": session_id,
        "type": session_state.state,
        "status": session_state.status,
        "status_remark": None,
    }

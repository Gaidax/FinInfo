from typing import List
from sqlalchemy.orm import Session
from app.models import SessionModel, SessionStateModel, SessionDataModel
from app.schemas.common import StepType, StepStatus


def get_session(db: Session, session_id: str) -> SessionModel:
    return db.query(SessionModel).filter(SessionModel.session_id == session_id).first()


def create_session(db: Session, session_id: str) -> SessionModel:
    session = SessionModel(session_id=session_id)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def ensure_session(db: Session, session_id: str) -> SessionModel:
    session = get_session(db=db, session_id=session_id)
    if session is None:
        session = create_session(db=db, session_id=session_id)
    return session


def get_session_state_list(db: Session, session_id: str, step: StepType) -> List[SessionStateModel]:
    return (
        db.query(SessionStateModel)
        .join(SessionModel)
        .filter(SessionModel.session_id == session_id, SessionStateModel.state == step)
        .all()
    )


def get_session_data_list(db: Session, session_id: str, tag: str) -> List[SessionDataModel]:
    return (
        db.query(SessionDataModel)
        .join(SessionModel)
        .filter(SessionModel.session_id == session_id, SessionDataModel.tag == tag)
        .all()
    )


def create_session_state(
    db: Session, session_id: str, step: StepType, status: StepStatus
):
    session = ensure_session(db=db, session_id=session_id)
    session_state = SessionStateModel(parent_id=session.id, state=step, status=status)
    db.add(session_state)
    db.commit()
    db.refresh(session_state)
    return session_state


def update_session_state(
    db: Session, session_state: SessionStateModel, status: StepStatus
):
    if session_state.status != status:
        session_state.status = status
        db.commit()
        db.refresh(session_state)
    return session_state


def create_session_data(db: Session, session_id: str, tag: str, data: dict):
    session = ensure_session(db=db, session_id=session_id)
    session_data = SessionDataModel(parent_id=session.id, tag=tag, data=data)
    db.add(session_data)
    db.commit()
    db.refresh(session_data)
    return session_data


def update_session_data(db: Session, session_data: SessionDataModel, data: dict):
    session_data.data = data
    db.commit()
    db.refresh(session_data)
    return session_data

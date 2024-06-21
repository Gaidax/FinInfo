from uuid import uuid4
from fastapi import APIRouter

router = APIRouter(prefix="/session", tags=["session"])


@router.post("")
async def create_session():
    return {"id": uuid4()}

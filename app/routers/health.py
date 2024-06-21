from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def health_check():
    return PlainTextResponse(content="I am healty", status_code=200)

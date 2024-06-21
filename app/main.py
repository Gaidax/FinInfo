from typing_extensions import Annotated
from fastapi import FastAPI, Request, status, HTTPException, Depends, Header
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from app.utils import rootLogger
from app.routers.health import router as health_router
from app.routers.pan import router as pan_router
from app.routers.eaadhaar import router as eaadhaar_router
from app.routers.session import router as session_router
from app.internal.session import Session
from app.routers.bank_accounts import router as bank_router
from app.routers.other_details import router as other_details_router


async def verify_token(session_id: Annotated[str, Header()], request: Request):
    """Global dependency to check session-id header in dynamodb"""
    if (
        session_id is None
        or Session.get_authenticated_subtoken_from_session_id(session_id) is None
    ):
        raise HTTPException(status_code=400, detail="session-id header invalid")

    # store in request.state if needed session id in routes
    request.state.session_id = session_id


app = FastAPI(dependencies=[Depends(verify_token)])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(pan_router)
app.include_router(eaadhaar_router)
app.include_router(session_router)
app.include_router(bank_router)
app.include_router(other_details_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Generic 422 validation exception handler for debug/development purposes"""
    rootLogger.error("422 EXCEPTION")
    rootLogger.error(exc.errors())
    return PlainTextResponse(str(exc), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

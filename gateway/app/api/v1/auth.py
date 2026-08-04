from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.schemas.token import LoginRequest
from app.services.auth_service import AuthService

router = APIRouter(tags=["Authentication"])


@router.post("/auth/login")
async def login(request: Request):
    body = await request.json()
    auth_service = AuthService(db=None)
    token = auth_service.login(LoginRequest(**body))

    return JSONResponse(
        status_code=200,
        content=token.model_dump(),
    )
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.token import LoginRequest, Token
from app.dependencies.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.health import HealthResponse
from app.schemas.response import APIResponse
from app.core.config import settings
from app.services.auth_service import AuthService

router = APIRouter()


@router.get(
    "/health",
    response_model=APIResponse,
    summary="Auth Service Health Check",
)
def health():
    return APIResponse(
        success=True,
        message="Auth Service is healthy",
        data=HealthResponse(
            status="healthy",
            service=settings.APP_NAME,
            version=settings.API_VERSION,
        ),
    )


@router.post(
    "/auth/register",
    response_model=UserResponse,
    status_code=201,
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    auth_service = AuthService(db)

    try:
        return auth_service.register(user)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.post(
    "/auth/login",
    response_model=Token,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    auth_service = AuthService(db)

    try:
        return auth_service.login(
            request.email,
            request.password,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )    
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import LoginRequest, Token
from app.services.auth_service import AuthService

router = APIRouter(tags=["Authentication"])


@router.post(
    "/auth/register",
    response_model=UserResponse,
    status_code=201,
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    return AuthService(db).register(user)


@router.post(
    "/auth/login",
    response_model=Token,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    return AuthService(db).login(request)
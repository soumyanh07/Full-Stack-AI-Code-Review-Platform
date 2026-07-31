from fastapi import HTTPException, status

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import LoginRequest, Token
from app.security.hashing import hash_password, verify_password
from app.security.jwt import create_access_token


class AuthService:
    def __init__(self, db):
        self.user_repository = UserRepository(db)

    def register(self, user: UserCreate) -> UserResponse:
        existing_user = self.user_repository.get_by_email(user.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        hashed = hash_password(user.password)

        db_user = self.user_repository.create(
            user=user,
            hashed_password=hashed,
        )

        return UserResponse.model_validate(db_user)

    def login(self, request: LoginRequest) -> Token:
        user = self.user_repository.get_by_email(request.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(
            request.password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        access_token = create_access_token(
            {
                "sub": user.email,
                "user_id": user.id,
            }
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
        )
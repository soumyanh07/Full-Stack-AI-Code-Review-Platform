from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.security.hashing import hash_password, verify_password
from app.security.jwt import create_access_token


class AuthService:
    def __init__(self, db):
        self.user_repository = UserRepository(db)

    def register(self, user: UserCreate) -> UserResponse:
        existing_user = self.user_repository.get_by_email(user.email)

        if existing_user:
            raise ValueError("Email already registered")

        hashed_password = hash_password(user.password)

        new_user = self.user_repository.create_user(
            name=user.name,
            email=user.email,
            hashed_password=hashed_password,
        )

        return UserResponse(
            id=new_user.id,
            name=new_user.name,
            email=new_user.email,
            created_at=new_user.created_at,
        )

    def login(self, email: str, password: str) -> Token:

        user = self.user_repository.get_by_email(email)

        if user is None:
            raise ValueError("Invalid email or password")

        # model stores hashed password in `hashed_password`
        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password")

        access_token = create_access_token(
            {"sub": user.email}
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
        )
import json
import urllib.error
import urllib.request

from fastapi import HTTPException, status

from app.core.config import settings
from app.schemas.token import LoginRequest, Token
from app.schemas.user import UserCreate, UserResponse


class AuthService:
    def __init__(self, db):
        self.db = db

    def _call_auth_service(self, path: str, payload: dict) -> dict:
        url = f"{settings.AUTH_SERVICE.rstrip('/')}/api/v1{path}"
        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8")
            try:
                detail_data = json.loads(detail)
                message = detail_data.get("detail", detail_data)
            except json.JSONDecodeError:
                message = detail or str(exc)

            raise HTTPException(
                status_code=exc.code,
                detail=message,
            ) from exc
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication service unavailable",
            ) from exc

    def register(self, user: UserCreate) -> UserResponse:
        payload = {
            "name": getattr(user, "name", user.username),
            "email": user.email,
            "password": user.password,
        }

        data = self._call_auth_service("/auth/register", payload)

        return UserResponse(
            id=data["id"],
            username=data.get("username") or data.get("name"),
            email=data["email"],
        )

    def login(self, request: LoginRequest) -> Token:
        payload = {
            "email": request.email,
            "password": request.password,
        }

        data = self._call_auth_service("/auth/login", payload)

        return Token(
            access_token=data["access_token"],
            token_type=data.get("token_type", "bearer"),
        )
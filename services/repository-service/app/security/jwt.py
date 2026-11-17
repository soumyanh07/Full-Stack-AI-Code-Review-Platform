from typing import Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.dependencies import get_db
from app.models.user import User


security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """Validate the JWT and resolve its subject to an active database user."""

    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise unauthorized

    try:
        payload: dict[str, Any] = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"require": ["exp", "sub"]},
        )
        user_id = int(payload["sub"])
        if user_id <= 0:
            raise ValueError("Invalid subject")
    except (InvalidTokenError, ValueError, TypeError, KeyError):
        raise unauthorized

    user = db.query(User).filter(User.id == user_id).first()

    if user is None or not user.is_active:
        raise unauthorized

    return user

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException, status
from jose import JWTError, jwt

from app.core.config import settings


def create_access_token(data: dict) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = data.copy()
    payload.update({"exp": expire})

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def verify_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
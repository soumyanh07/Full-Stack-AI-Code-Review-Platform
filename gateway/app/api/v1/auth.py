import json
import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.utils.proxy import ProxyClient

logger = logging.getLogger("gateway.auth")
router = APIRouter(tags=["Authentication"])


async def _read_json_body(request: Request) -> dict:
    raw_body = await request.body()
    if not raw_body:
        return {}

    try:
        return json.loads(raw_body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Invalid JSON body") from exc


@router.post("/auth/register")
async def register(request: Request):
    try:
        body = await _read_json_body(request)
    except ValueError as exc:
        logger.warning("Invalid register payload: %s", exc)
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    try:
        data, status = await ProxyClient.forward(
            method="POST",
            url=f"{settings.AUTH_SERVICE}/api/v1/auth/register",
            body=body,
        )
    except Exception:
        logger.exception("Unexpected error while proxying register request")
        return JSONResponse(status_code=500, content={"detail": "Internal gateway error"})

    return JSONResponse(status_code=status, content=data)


@router.post("/auth/login")
async def login(request: Request):
    try:
        body = await _read_json_body(request)
    except ValueError as exc:
        logger.warning("Invalid login payload: %s", exc)
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    try:
        data, status = await ProxyClient.forward(
            method="POST",
            url=f"{settings.AUTH_SERVICE}/api/v1/auth/login",
            body=body,
        )
    except Exception:
        logger.exception("Unexpected error while proxying login request")
        return JSONResponse(status_code=500, content={"detail": "Internal gateway error"})

    return JSONResponse(status_code=status, content=data)
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.utils.proxy import ProxyClient

router = APIRouter(tags=["Authentication"])


@router.post("/auth/login")
async def login(request: Request):
    body = await request.json()
    data, status_code = await ProxyClient.forward(
        method="POST",
        url=f"{settings.AUTH_SERVICE.rstrip('/')}/api/v1/auth/login",
        headers={"Content-Type": "application/json"},
        body=body,
    )
    return JSONResponse(status_code=status_code, content=data)

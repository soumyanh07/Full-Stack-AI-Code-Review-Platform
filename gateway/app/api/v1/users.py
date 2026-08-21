from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.utils.proxy import ProxyClient

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me")
async def get_me(request: Request):
    try:
        data, status = await ProxyClient.forward(
            method="GET",
            url=f"{settings.AUTH_SERVICE}/api/v1/auth/me",
            headers={
                key: value
                for key, value in request.headers.items()
                if key.lower() == "authorization"
            },
        )

        return JSONResponse(
            status_code=status,
            content=data,
        )

    except Exception:
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal gateway error"},
        )

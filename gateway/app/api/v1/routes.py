
from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.core.config import settings
from app.schemas.health import HealthResponse
from app.schemas.response import APIResponse

router = APIRouter(tags=["Gateway"])

router.include_router(auth_router)
router.include_router(users_router)


@router.get(
    "/health",
    response_model=APIResponse,
    summary="Gateway Health Check",
)
async def health():
    return APIResponse(
        success=True,
        message="Gateway is healthy",
        data=HealthResponse(
            status="healthy",
            service=settings.APP_NAME,
            version=settings.API_VERSION,
        ),
    )
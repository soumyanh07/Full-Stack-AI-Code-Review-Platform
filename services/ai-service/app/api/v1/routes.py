from fastapi import APIRouter

from app.schemas.ai import AnalyzeRequest, AnalyzeResponse
from app.services.ollama_service import OllamaService

router = APIRouter()

service = OllamaService()


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
)
def analyze(request: AnalyzeRequest):
    return service.analyze(request)
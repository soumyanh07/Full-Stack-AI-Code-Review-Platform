import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.services.repository_service import RepositoryService
from app.security.jwt import get_current_user


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["AI Chat"])


@router.post("", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        RepositoryService(db).get_repository(
            request.repository_id,
            owner_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Repository not found.") from exc

    try:
        return ChatService().chat(
            repository_id=request.repository_id,
            question=request.question,
        )
    except Exception:
        logger.exception("Repository chat failed for repository %s", request.repository_id)
        raise HTTPException(status_code=500, detail="Unable to process repository chat.")

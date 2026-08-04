from app.api.v1.webhook import router as webhook_router
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.dependencies.database import get_db
from app.schemas.pull_request import PullRequestReviewRequest
from app.services.pr_review_service import PRReviewService
from app.schemas.repository import (
    RepositoryCreate,
    RepositoryResponse,
)
from app.services.repository_service import RepositoryService

router = APIRouter()


@router.get("/")
def root():
    return {
        "service": "Repository Service",
        "status": "running",
    }


@router.get(
    "/repositories",
    response_model=list[RepositoryResponse],
)
def get_repositories(
    db: Session = Depends(get_db),
):
    service = RepositoryService(db)
    return service.get_repositories()


@router.post(
    "/repositories",
    response_model=RepositoryResponse,
    status_code=201,
)
def create_repository(
    repository: RepositoryCreate,
    db: Session = Depends(get_db),
):
    service = RepositoryService(db)
    return service.create_repository(repository)


@router.get(
    "/repositories/{repo_id}",
    response_model=RepositoryResponse,
)
def get_repository(
    repo_id: int,
    db: Session = Depends(get_db),
):
    service = RepositoryService(db)
    return service.get_repository(repo_id)

@router.post(
    "/chat",
    response_model=ChatResponse,
    tags=["Repository Chat"],
)
def chat(request: ChatRequest):
    service = ChatService()

    answer = service.chat(
        repository_id=request.repository_id,
        question=request.question,
    )

    return ChatResponse(
        answer=answer,
    )



@router.post(
    "/pull-request/review",
    tags=["Pull Request Review"],
)
def review_pull_request(
    request: PullRequestReviewRequest,
):
    service = PRReviewService()

    return service.review_pull_request(
        repository=request.repository,
        pr_number=request.pr_number,
    )


router.include_router(
    webhook_router,
)
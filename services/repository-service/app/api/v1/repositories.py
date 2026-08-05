from fastapi import APIRouter, Header, HTTPException

from app.services.repository_service import RepositoryService

router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"],
)


def get_token(authorization: str = Header(...)) -> str:
    """
    Extract GitHub access token from Authorization header.
    Expected format:
    Authorization: Bearer <token>
    """

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid Authorization header",
        )

    return authorization.split(" ", 1)[1]


@router.get("")
async def list_repositories(
    token: str = Header(..., alias="Authorization"),
):
    service = RepositoryService(get_token(token))
    return await service.list_repositories()


@router.get("/{owner}/{repo}")
async def repository_details(
    owner: str,
    repo: str,
    token: str = Header(..., alias="Authorization"),
):
    service = RepositoryService(get_token(token))
    return await service.get_repository(owner, repo)


@router.get("/{owner}/{repo}/branches")
async def branches(
    owner: str,
    repo: str,
    token: str = Header(..., alias="Authorization"),
):
    service = RepositoryService(get_token(token))
    return await service.list_branches(owner, repo)


@router.get("/{owner}/{repo}/pulls")
async def pull_requests(
    owner: str,
    repo: str,
    token: str = Header(..., alias="Authorization"),
):
    service = RepositoryService(get_token(token))
    return await service.list_pull_requests(owner, repo)


@router.get("/{owner}/{repo}/files")
async def repository_files(
    owner: str,
    repo: str,
    path: str = "",
    token: str = Header(..., alias="Authorization"),
):
    service = RepositoryService(get_token(token))
    return await service.list_files(
        owner,
        repo,
        path,
    )
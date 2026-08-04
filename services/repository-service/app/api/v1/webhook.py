from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/github/webhook")
async def github_webhook(request: Request):
    payload = await request.json()

    print("=" * 60)
    print("GitHub Webhook Received")
    print("=" * 60)

    print(payload)

    return {
        "status": "received"
    }
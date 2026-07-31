from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def register_cors(app: FastAPI) -> None:
    """
    Register CORS middleware.
    """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Replace with frontend URL in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
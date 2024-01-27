from fastapi import FastAPI
from router import api_router
from fastapi.middleware.cors import CORSMiddleware

def app() -> FastAPI:
    app = FastAPI(title="Lighter app")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router=api_router, prefix="/api")
    return app


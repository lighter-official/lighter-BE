from fastapi import FastAPI
from router import api_router

def app() -> FastAPI:
    app = FastAPI(title="Lighter app")
    app.include_router(router=api_router, prefix="/api")
    return app


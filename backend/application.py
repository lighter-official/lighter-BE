from fastapi import FastAPI
from router import api_router
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Depends, FastAPI, Header, Query, Request, HTTPException, status
from starlette.templating import Jinja2Templates
from backend.examples.tutorial import get_oauth_client
import secrets

def app() -> FastAPI:
    app = FastAPI(title="Gloo")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    templates = Jinja2Templates(directory="templates")

    @app.get("/", response_class=HTMLResponse)
    async def login(request: Request):
        return templates.TemplateResponse("login.html", {"request": request})

    @app.get("/login")
    async def login_naver(oauth_client=Depends(get_oauth_client)):
        state = secrets.token_urlsafe(32)
        login_url = oauth_client.get_oauth_login_url(state=state)
        return RedirectResponse(login_url)

    app.include_router(router=api_router, prefix="/api")
    return app


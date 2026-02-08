from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.repository_factory import create_repositories
from src.infrastructure.security.jwt_service import JWTService
from src.infrastructure.settings import load_settings
from src.web.framework.routes.auth_routes import auth_routes
from src.web.framework.routes.chat_routes import chat_routes
from src.web.framework.routes.company_routes import company_routes
from src.web.framework.routes.contact_routes import contact_routes
from src.web.framework.routes.message_routes import message_routes
from src.web.framework.routes.readiness_routes import readiness_routes
from src.web.framework.routes.user_routes import user_routes
from src.web.framework.routes.webhook_routes import webhook_routes
from src.web.middleware.auth_middleware import auth_middleware


def create_app() -> FastAPI:
    app = FastAPI(title="Convo API")

    app.include_router(readiness_routes)
    app.include_router(auth_routes)
    app.include_router(user_routes)
    app.include_router(company_routes)
    app.include_router(contact_routes)
    app.include_router(chat_routes)
    app.include_router(message_routes)
    app.include_router(webhook_routes)

    app.state.settings = load_settings()
    app.state.jwt_service = JWTService(settings=app.state.settings)

    repositories = create_repositories(settings=app.state.settings)

    app.state.user_repository = repositories["user"]
    app.state.company_repository = repositories["company"]
    app.state.contact_repository = repositories["contact"]
    app.state.chat_repository = repositories["chat"]
    app.state.message_repository = repositories["message"]

    origins = app.state.settings.CORS_ORIGINS

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.middleware("http")(auth_middleware)

    return app


app = create_app()

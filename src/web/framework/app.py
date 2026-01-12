from fastapi import FastAPI

from src.web.framework.routes.chat_routes import chat_routes
from src.web.framework.routes.company_routes import company_routes
from src.web.framework.routes.contact_routes import contact_routes
from src.web.framework.routes.message_routes import message_routes
from src.web.framework.routes.readiness_routes import readiness_routes
from src.web.framework.routes.user_routes import user_routes
from src.web.framework.routes.webhook_routes import webhook_routes
from tests.fakes.repositories.fake_in_memory_chat_repository import (
    InMemoryChatRepository,
)
from tests.fakes.repositories.fake_in_memory_company_repository import (
    InMemoryCompanyRepository,
)
from tests.fakes.repositories.fake_in_memory_contact_repository import (
    InMemoryContactRepository,
)
from tests.fakes.repositories.fake_in_memory_message_repository import (
    InMemoryMessageRepository,
)
from tests.fakes.repositories.fake_in_memory_user_repository import (
    InMemoryUserRepository,
)


def create_app() -> FastAPI:
    app = FastAPI(title="Convo API")

    app.include_router(readiness_routes)
    app.include_router(user_routes)
    app.include_router(company_routes)
    app.include_router(contact_routes)
    app.include_router(chat_routes)
    app.include_router(message_routes)
    app.include_router(webhook_routes)

    # setup_sqlite_converters()
    # DATABASE_NAME = "app.db"
    # user_dao = SQLiteUserDAO(DATABASE_NAME)
    # app.config["user_repository"] = SQLiteUserRepository(user_dao=user_dao)
    #
    # company_dao = SQLiteCompanyDAO(DATABASE_NAME)
    # app.config["company_repository"] = SQLiteCompanyRepository(company_dao=company_dao)

    app.state.user_repository = InMemoryUserRepository()
    app.state.company_repository = InMemoryCompanyRepository()
    app.state.contact_repository = InMemoryContactRepository()
    app.state.chat_repository = InMemoryChatRepository()
    app.state.message_repository = InMemoryMessageRepository()

    return app


app = create_app()

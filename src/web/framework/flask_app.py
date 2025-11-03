from flask import Flask

from src.web.framework.routes.chat_routes import chat_route_blueprint
from src.web.framework.routes.company_routes import company_route_blueprint
from src.web.framework.routes.contact_routes import contact_route_blueprint
from src.web.framework.routes.message_routes import message_route_blueprint
from src.web.framework.routes.user_routes import user_route_blueprint
from tests.fakes.repositories.in_memory_chat_repository import (
    InMemoryChatRepository,
)
from tests.fakes.repositories.in_memory_company_repository import (
    InMemoryCompanyRepository,
)
from tests.fakes.repositories.in_memory_contact_repository import (
    InMemoryContactRepository,
)
from tests.fakes.repositories.in_memory_message_repository import (
    InMemoryMessageRepository,
)
from tests.fakes.repositories.in_memory_user_repository import (
    InMemoryUserRepository,
)

DATABASE_NAME = "app.db"


def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_route_blueprint, url_prefix="/users")
    app.register_blueprint(company_route_blueprint, url_prefix="/companies")
    app.register_blueprint(chat_route_blueprint, url_prefix="/chats")
    app.register_blueprint(message_route_blueprint, url_prefix="/messages")
    app.register_blueprint(contact_route_blueprint, url_prefix="/contacts")

    # user_dao = SQLiteUserDAO(DATABASE_NAME)
    # app.config["user_repository"] = SQLiteUserRepository(user_dao=user_dao)
    #
    # company_dao = SQLiteCompanyDAO(DATABASE_NAME)
    # app.config["company_repository"] = SQLiteCompanyRepository(company_dao=company_dao)

    app.config["user_repository"] = InMemoryUserRepository()
    app.config["company_repository"] = InMemoryCompanyRepository()
    app.config["contact_repository"] = InMemoryContactRepository()
    app.config["chat_repository"] = InMemoryChatRepository()
    app.config["message_repository"] = InMemoryMessageRepository()

    return app

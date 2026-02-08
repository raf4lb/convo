from src.infrastructure.daos.chat_dao import SQLiteChatDAO
from src.infrastructure.daos.company_dao import SQLiteCompanyDAO
from src.infrastructure.daos.contact_dao import SQLiteContactDAO
from src.infrastructure.daos.postgres_chat_dao import PostgresChatDAO
from src.infrastructure.daos.postgres_company_dao import PostgresCompanyDAO
from src.infrastructure.daos.postgres_contact_dao import PostgresContactDAO
from src.infrastructure.daos.postgres_message_dao import PostgresMessageDAO
from src.infrastructure.daos.postgres_user_dao import PostgresUserDAO
from src.infrastructure.daos.user_dao import SQLiteUserDAO
from src.infrastructure.database.sqlite_setup import setup_sqlite_converters
from src.infrastructure.enums import DatabaseType
from src.infrastructure.repositories.postgres_chat_repository import (
    PostgresChatRepository,
)
from src.infrastructure.repositories.postgres_company_repository import (
    PostgresCompanyRepository,
)
from src.infrastructure.repositories.postgres_contact_repository import (
    PostgresContactRepository,
)
from src.infrastructure.repositories.postgres_message_repository import (
    PostgresMessageRepository,
)
from src.infrastructure.repositories.postgres_user_repository import (
    PostgresUserRepository,
)
from src.infrastructure.repositories.sqlite_chat_repository import (
    SQLiteChatRepository,
)
from src.infrastructure.repositories.sqlite_company_repository import (
    SQLiteCompanyRepository,
)
from src.infrastructure.repositories.sqlite_contact_repository import (
    SQLiteContactRepository,
)
from src.infrastructure.repositories.sqlite_user_repository import (
    SQLiteUserRepository,
)
from src.infrastructure.settings import AppSettings
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


def create_repositories(settings: AppSettings) -> dict:
    """
    Factory function to create all repositories based on database type.

    Args:
        settings: Application settings containing database configuration
                  (database type is extracted from settings.DATABASE_TYPE)

    Returns:
        Dictionary with repository instances:
        {
            "user": IUserRepository,
            "company": ICompanyRepository,
            "contact": IContactRepository,
            "chat": IChatRepository,
            "message": IMessageRepository
        }
    """
    database_type = settings.DATABASE_TYPE

    if database_type == DatabaseType.SQLITE:
        setup_sqlite_converters()
        db_path = settings.DATABASE_NAME

        user_dao = SQLiteUserDAO(db_path)
        company_dao = SQLiteCompanyDAO(db_path)
        contact_dao = SQLiteContactDAO(db_path)
        chat_dao = SQLiteChatDAO(db_path)

        return {
            "user": SQLiteUserRepository(user_dao),
            "company": SQLiteCompanyRepository(company_dao),
            "contact": SQLiteContactRepository(contact_dao),
            "chat": SQLiteChatRepository(chat_dao),
            "message": InMemoryMessageRepository(),
        }

    elif database_type == DatabaseType.POSTGRES:
        database_url = settings.DATABASE_URL

        user_dao = PostgresUserDAO(database_url)
        company_dao = PostgresCompanyDAO(database_url)
        contact_dao = PostgresContactDAO(database_url)
        chat_dao = PostgresChatDAO(database_url)
        message_dao = PostgresMessageDAO(database_url)

        return {
            "user": PostgresUserRepository(user_dao),
            "company": PostgresCompanyRepository(company_dao),
            "contact": PostgresContactRepository(contact_dao),
            "chat": PostgresChatRepository(chat_dao),
            "message": PostgresMessageRepository(message_dao),
        }

    elif database_type == DatabaseType.INMEMORY:
        return {
            "user": InMemoryUserRepository(),
            "company": InMemoryCompanyRepository(),
            "contact": InMemoryContactRepository(),
            "chat": InMemoryChatRepository(),
            "message": InMemoryMessageRepository(),
        }

    else:
        raise ValueError(
            f"Invalid database type: {database_type}. "
            f"Valid options: {', '.join([t.value for t in DatabaseType])}"
        )

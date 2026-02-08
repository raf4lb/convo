from src.domain.entities.user import User
from src.domain.enums import UserTypes
from src.domain.errors import UserNotFoundError
from src.domain.repositories.user_repository import IUserRepository
from src.infrastructure.daos.postgres_user_dao import PostgresUserDAO


class PostgresUserRepository(IUserRepository):
    def __init__(self, user_dao: PostgresUserDAO):
        self.user_dao = user_dao

    @staticmethod
    def _parse_row(row: tuple) -> User:
        """Parse row from get_by_id or get_all (without password_hash)."""
        return User(
            id=row[0],
            name=row[1],
            email=row[2],
            type=UserTypes(row[3]),
            password_hash=None,
            company_id=row[4],
            is_active=row[5],
            created_at=row[6],
            updated_at=row[7],
        )

    @staticmethod
    def _parse_row_with_password(row: tuple) -> User:
        """Parse row from get_by_email (with password_hash)."""
        return User(
            id=row[0],
            name=row[1],
            email=row[2],
            type=UserTypes(row[3]),
            password_hash=row[4],
            company_id=row[5],
            is_active=row[6],
            created_at=row[7],
            updated_at=row[8],
        )

    def save(self, user: User) -> None:
        existing = self.user_dao.get_by_id(user_id=user.id)
        user_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "type": user.type.value,
            "password_hash": user.password_hash,
            "company_id": user.company_id,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }

        if existing:
            self.user_dao.update(user_data)
        else:
            self.user_dao.insert(user_data)

    def get_by_id(self, user_id: str) -> User:
        row = self.user_dao.get_by_id(user_id=user_id)
        if not row:
            raise UserNotFoundError

        return self._parse_row(row=row)

    def get_by_email(self, email: str) -> User:
        row = self.user_dao.get_by_email(email=email)
        if not row:
            raise UserNotFoundError

        return self._parse_row_with_password(row=row)

    def get_all(self) -> list[User]:
        rows = self.user_dao.get_all()
        return [self._parse_row(row=row) for row in rows]

    def delete(self, user_id: str) -> None:
        self.get_by_id(user_id=user_id)
        self.user_dao.delete(user_id=user_id)

    def update_password(self, user_id: str, password_hash: str) -> None:
        """Update only the password for a user."""
        self.get_by_id(user_id=user_id)  # Verify user exists
        self.user_dao.update_password(user_id=user_id, password_hash=password_hash)

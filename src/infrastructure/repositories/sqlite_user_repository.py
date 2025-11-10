from src.domain.entities.user import User
from src.domain.errors import UserNotFoundError
from src.domain.repositories.user_repository import IUserRepository
from src.infrastructure.daos.user_dao import SQLiteUserDAO


class SQLiteUserRepository(IUserRepository):
    def __init__(self, user_dao: SQLiteUserDAO):
        self.user_dao = user_dao

    @staticmethod
    def _parse_row(row: tuple) -> User:
        return User(
            id=row[0],
            name=row[1],
            email=row[2],
            type=row[3],
            company_id=row[4],
            created_at=row[5],
            updated_at=row[6],
        )

    def save(self, user: User) -> None:
        existing = self.user_dao.get_by_id(user_id=user.id)
        user_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "type": user.type.value,
            "company_id": user.company_id,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }

        if existing:
            self.user_dao.update(user_data)
        else:
            self.user_dao.insert(user_data)

    def get_by_id(self, user_id: str) -> User | None:
        row = self.user_dao.get_by_id(user_id=user_id)
        if not row:
            raise UserNotFoundError

        return self._parse_row(row=row)

    def get_all(self) -> list[User]:
        rows = self.user_dao.get_all()
        return [self._parse_row(row=row) for row in rows]

    def delete(self, user_id: str) -> None:
        self.get_by_id(user_id=user_id)
        self.user_dao.delete(user_id=user_id)

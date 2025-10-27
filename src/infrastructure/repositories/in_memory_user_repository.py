from src.domain.entities.user import User
from src.domain.errors import UserNotFoundError
from src.domain.repositories.user_repository import IUserRepository


class InMemoryUserRepository(IUserRepository):
    def __init__(self):
        self.users = {}

    def save(self, user: User) -> None:
        self.users[user.id] = user

    def get_user_by_id(self, user_id: str) -> User | None:
        user = self.users.get(user_id)
        if user is None:
            raise UserNotFoundError
        return user

    def get_users(self) -> list[User]:
        return list(self.users.values())

    def delete(self, company_id: str) -> None:
        try:
            self.users.pop(company_id)
        except KeyError:
            raise UserNotFoundError

from src.domain.entities.user import User
from src.domain.errors import UserNotFoundError
from src.domain.repositories.user_repository import IUserRepository


class InMemoryUserRepository(IUserRepository):
    def __init__(self):
        self.users = {}

    def save(self, user: User) -> User:
        self.users[user.id] = user
        return user

    def get_by_id(self, user_id: str) -> User | None:
        user = self.users.get(user_id)
        if user is None:
            raise UserNotFoundError
        return user

    def get_all(self) -> list[User]:
        return list(self.users.values())

    def delete(self, user_id: str) -> None:
        self.users.pop(user_id, None)

import uuid

from src.application.exceptions import UserNotFoundError
from src.application.interfaces.user_repository_interface import UserRepositoryInterface
from src.domain.entities.user import User


class InMemoryUserRepository(UserRepositoryInterface):
    def __init__(self):
        self.users = {}

    def create_user(self, user: User) -> None:
        self.users[user.id] = user

    def update_user(self, user: User) -> None:
        if user.id not in self.users:
            raise UserNotFoundError(f"user {user.id} not found")
        self.users[user.id] = user

    def get_user_by_id(self, user_id: uuid.UUID) -> User:
        return self.users.get(user_id)

    def get_users(self) -> list[User]:
        return list(self.users.values())

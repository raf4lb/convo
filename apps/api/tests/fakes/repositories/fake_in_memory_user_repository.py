from src.domain.entities.user import User
from src.domain.enums import UserTypes
from src.domain.errors import UserNotFoundError
from src.domain.repositories.user_repository import IUserRepository


class InMemoryUserRepository(IUserRepository):
    def __init__(self):
        self.users = {}

    def save(self, user: User) -> User:
        self.users[user.id] = user
        return user

    def get_by_id(self, user_id: str) -> User:
        user = self.users.get(user_id)
        if user is None:
            raise UserNotFoundError
        return user

    def get_by_email(self, email: str) -> User:
        for user in self.users.values():
            if user.email == email:
                return user
        raise UserNotFoundError

    def get_all(self) -> list[User]:
        return list(self.users.values())

    def delete(self, user_id: str) -> None:
        self.get_by_id(user_id=user_id)
        self.users.pop(user_id)

    def update_password(self, user_id: str, password_hash: str) -> None:
        user = self.get_by_id(user_id)
        user.password_hash = password_hash
        self.save(user)

    def get_by_company_id(self, company_id: str) -> list[User]:
        return [user for user in self.users.values() if user.company_id == company_id]

    def get_by_company_and_role(self, company_id: str, role: UserTypes) -> list[User]:
        return [
            user
            for user in self.users.values()
            if user.company_id == company_id and user.type == role
        ]

    def search_users(
        self, company_id: str, query: str, role: UserTypes | None = None
    ) -> list[User]:
        results = []
        query_lower = query.lower()
        for user in self.users.values():
            if user.company_id != company_id:
                continue
            if role and user.type != role:
                continue
            if query_lower in user.name.lower() or query_lower in user.email.lower():
                results.append(user)
        return results

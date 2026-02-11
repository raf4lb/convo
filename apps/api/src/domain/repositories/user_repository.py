from abc import ABC, abstractmethod

from src.domain.entities.user import User
from src.domain.enums import UserTypes


class IUserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User: ...

    @abstractmethod
    def get_by_id(self, user_id: str) -> User: ...

    @abstractmethod
    def get_by_email(self, email: str) -> User: ...

    @abstractmethod
    def get_all(self) -> list[User]: ...

    @abstractmethod
    def delete(self, user_id: str) -> None: ...

    @abstractmethod
    def update_password(self, user_id: str, password_hash: str) -> None: ...

    @abstractmethod
    def get_by_company_id(self, company_id: str) -> list[User]: ...

    @abstractmethod
    def get_by_company_and_role(
        self, company_id: str, role: UserTypes
    ) -> list[User]: ...

    @abstractmethod
    def search_users(
        self, company_id: str, query: str, role: UserTypes | None = None
    ) -> list[User]: ...

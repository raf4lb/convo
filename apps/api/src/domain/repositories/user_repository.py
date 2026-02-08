from abc import ABC, abstractmethod

from src.domain.entities.user import User


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

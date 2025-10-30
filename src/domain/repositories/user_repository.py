from abc import ABC, abstractmethod

from src.domain.entities.user import User


class IUserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None: ...

    @abstractmethod
    def get_by_id(self, user_id: str) -> User | None: ...

    @abstractmethod
    def get_users(self) -> list[User]: ...

    @abstractmethod
    def delete(self, user_id: str) -> None: ...

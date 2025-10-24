import uuid
from abc import ABC, abstractmethod

from src.domain.entities.company import Company
from src.domain.entities.user import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    def create_user(self, user: User) -> None: ...

    @abstractmethod
    def update_user(self, user: User) -> None: ...

    @abstractmethod
    def get_user_by_id(self, user_id: uuid.UUID) -> User: ...

    @abstractmethod
    def get_users(self) -> list[User]: ...


class CompanyRepositoryInterface(ABC):
    @abstractmethod
    def create_company(self, company: Company) -> None: ...

    @abstractmethod
    def update_company(self, company: Company) -> None: ...

    @abstractmethod
    def get_company_by_id(self, company_id: uuid.UUID) -> Company: ...

    @abstractmethod
    def get_companies(self) -> list[Company]: ...

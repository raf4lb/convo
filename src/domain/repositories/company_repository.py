from abc import ABC, abstractmethod

from src.domain.entities.company import Company


class ICompanyRepository(ABC):
    @abstractmethod
    def save(self, company: Company) -> None: ...

    @abstractmethod
    def get_by_id(self, company_id: str) -> Company | None: ...

    @abstractmethod
    def get_companies(self) -> list[Company]: ...

    @abstractmethod
    def delete(self, company_id: str) -> None: ...

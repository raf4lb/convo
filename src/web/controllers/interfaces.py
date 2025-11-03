from abc import ABC, abstractmethod

from src.domain.repositories.chat_repository import IChatRepository
from src.domain.repositories.company_repository import ICompanyRepository
from src.domain.repositories.contact_repository import IContactRepository
from src.domain.repositories.message_repository import IMessageRepository
from src.domain.repositories.user_repository import IUserRepository
from src.web.controllers.http_types import HttpRequest, HttpResponse


class IUserHttpController(ABC):
    def __init__(self, user_repository: IUserRepository):
        self._repository = user_repository

    @abstractmethod
    def handle(self, request: HttpRequest) -> HttpResponse: ...


class ICompanyHttpController(ABC):
    def __init__(self, company_repository: ICompanyRepository):
        self._repository = company_repository

    @abstractmethod
    def handle(self, request: HttpRequest) -> HttpResponse: ...


class IContactHttpController(ABC):
    def __init__(self, contact_repository: IContactRepository):
        self._contact_repository = contact_repository

    @abstractmethod
    def handle(self, request: HttpRequest) -> HttpResponse: ...


class IChatHttpController(ABC):
    def __init__(self, chat_repository: IChatRepository):
        self._chat_repository = chat_repository

    @abstractmethod
    def handle(self, request: HttpRequest) -> HttpResponse: ...


class IMessageHttpController(ABC):
    def __init__(self, message_repository: IMessageRepository):
        self._message_repository = message_repository

    @abstractmethod
    def handle(self, request: HttpRequest) -> HttpResponse: ...

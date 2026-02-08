from abc import ABC, abstractmethod

from src.domain.repositories.chat_repository import IChatRepository
from src.domain.repositories.company_repository import ICompanyRepository
from src.domain.repositories.contact_repository import IContactRepository
from src.domain.repositories.message_repository import IMessageRepository
from src.domain.repositories.user_repository import IUserRepository


class IUserUseCase(ABC):
    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository

    @abstractmethod
    def execute(self, *args, **kwargs): ...


class ICompanyUseCase(ABC):
    def __init__(self, company_repository: ICompanyRepository):
        self._company_repository = company_repository

    @abstractmethod
    def execute(self, *args, **kwargs): ...


class IMessageUseCase(ABC):
    def __init__(self, message_repository: IMessageRepository):
        self._message_repository = message_repository

    @abstractmethod
    def execute(self, *args, **kwargs): ...


class IContactUseCase(ABC):
    def __init__(self, contact_repository: IContactRepository):
        self._contact_repository = contact_repository

    @abstractmethod
    def execute(self, *args, **kwargs): ...


class IChatUseCase(ABC):
    def __init__(self, chat_repository: IChatRepository):
        self._chat_repository = chat_repository

    @abstractmethod
    def execute(self, *args, **kwargs): ...

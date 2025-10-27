import uuid

from src.application.interfaces.use_case_interface import IUseCase
from src.domain.entities.user import User
from src.domain.enums import UserTypes
from src.domain.repositories.user_repository import IUserRepository
from src.helpers.helpes import get_now_iso_format


class CreateUserUseCase(IUseCase):
    def __init__(self, repository: IUserRepository):
        self._repository = repository

    def execute(
        self,
        name: str,
        email: str,
        type: UserTypes,
        company_id: str,
    ) -> User:
        created_at = get_now_iso_format()
        user = User(
            id=str(uuid.uuid4()),
            name=name,
            email=email,
            type=type,
            company_id=company_id,
            created_at=created_at,
            updated_at=created_at,
        )
        self._repository.save(user)
        return user


class UpdateUserUseCase(IUseCase):
    def __init__(self, repository: IUserRepository):
        self._repository = repository

    def execute(
        self,
        user_id: str,
        name: str,
        email: str,
        type: UserTypes,
        company_id: str,
    ) -> User:
        user = self._repository.get_user_by_id(user_id)
        user.name = name
        user.email = email
        user.type = type
        user.company_id = company_id
        user.updated_at = get_now_iso_format()
        self._repository.save(user)
        return user

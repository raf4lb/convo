from src.application.exceptions import InvalidUserError
from src.application.interfaces import IUserUseCase
from src.domain.entities.user import User
from src.domain.enums import UserTypes
from src.domain.errors import CompanyNotFoundError
from src.domain.repositories.company_repository import ICompanyRepository
from src.domain.repositories.user_repository import IUserRepository
from src.helpers.helpers import generate_uuid4, get_now


class CreateUserUseCase(IUserUseCase):
    def __init__(
        self,
        user_repository: IUserRepository,
        company_repository: ICompanyRepository,
    ):
        super().__init__(user_repository=user_repository)
        self._company_repository = company_repository

    def _is_valid_company(self, company_id: str) -> bool:
        try:
            return bool(self._company_repository.get_by_id(company_id))
        except CompanyNotFoundError:
            return False

    def _validate(self, user: User) -> list[str]:
        errors = []
        if user_errors := user.validate():
            errors.extend(user_errors)
        if user.company_id and not self._is_valid_company(user.company_id):
            errors.append("Invalid company id")
        return errors

    def execute(
        self,
        name: str,
        email: str,
        type: UserTypes,
        company_id: str | None = None,
    ) -> User:
        user = User(
            id=generate_uuid4(),
            name=name,
            email=email,
            type=type,
            company_id=company_id,
        )

        if errors := self._validate(user):
            print(errors)
            raise InvalidUserError(errors=errors)

        self._user_repository.save(user)
        return user


class UpdateUserUseCase(IUserUseCase):
    def execute(
        self,
        user_id: str,
        name: str,
        email: str,
        type: UserTypes,
    ) -> User:
        user = self._user_repository.get_by_id(user_id)
        user.name = name
        user.email = email
        user.type = type
        user.updated_at = get_now()
        self._user_repository.save(user)
        return user


class GetUserUseCase(IUserUseCase):
    def execute(self, user_id) -> User:
        return self._user_repository.get_by_id(user_id=user_id)


class DeleteUserUseCase(IUserUseCase):
    def execute(self, user_id: str) -> None:
        self._user_repository.delete(user_id)


class ListUserUseCase(IUserUseCase):
    def execute(self) -> list[User]:
        return self._user_repository.get_all()

from src.application.interfaces.use_case_interface import UseCaseInterface
from src.application.interfaces.user_repository_interface import UserRepositoryInterface
from src.domain.entities.user import User


class CreateUserUseCase(UseCaseInterface):
    def __init__(self, repository: UserRepositoryInterface):
        self._repository = repository

    def execute(self, user: User) -> None:
        self._repository.create_user(user)


class UpdateUserUseCase(UseCaseInterface):
    def __init__(self, repository: UserRepositoryInterface):
        self._repository = repository

    def execute(self, user: User) -> None:
        self._repository.update_user(user)

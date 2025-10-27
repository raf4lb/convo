from src.domain.enums import UserTypes


class User:
    def __init__(
        self,
        id: str,
        name: str,
        email: str,
        type: UserTypes,
        company_id: str,
        created_at: str,
        updated_at: str,
    ):
        self.id = id
        self.name = name
        self.email = email
        self.type = type
        self.company_id = company_id
        self.created_at = created_at
        self.updated_at = updated_at

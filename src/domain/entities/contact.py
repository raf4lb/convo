class Contact:
    def __init__(
        self,
        id: str,
        name: str,
        phone_number: str,
        created_at: str,
        updated_at: str,
        company_id: str | None = None,
    ):
        self.id = id
        self.company_id = company_id
        self.name = name
        self.phone_number = phone_number
        self.created_at = created_at
        self.updated_at = updated_at

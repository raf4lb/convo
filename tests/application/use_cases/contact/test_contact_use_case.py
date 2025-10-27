import uuid

import pytest

from src.application.use_cases.contact.contact_use_cases import (
    CreateContactUseCase,
    UpdateContactUseCase,
)
from src.domain.errors import ContactNotFoundError


def test_create_contact_use_case(contact_repository):
    # Arrange
    use_case = CreateContactUseCase(repository=contact_repository)

    # Act
    contact = use_case.execute(
        name="Contact Name",
        phone_number="+558899034444",
        company_id=str(uuid.uuid4()),
    )

    # Assert
    assert contact_repository.get_contact_by_id(contact.id)


def test_update_contact_use_case_existing_company(contact, contact_repository):
    # Arrange
    contact_repository.save(contact)
    use_case = UpdateContactUseCase(repository=contact_repository)

    # Act
    new_name = "New Name"
    contact = use_case.execute(
        contact_id=contact.id,
        name=new_name,
        phone_number=contact.phone_number,
        company_id=contact.company_id,
    )

    # Assert
    assert contact.name == new_name


def test_update_contact_use_case_non_existing_company(contact, contact_repository):
    # Arrange
    use_case = UpdateContactUseCase(repository=contact_repository)

    # Act/Assert
    with pytest.raises(ContactNotFoundError):
        use_case.execute(
            contact_id=contact.id,
            name="New Name",
            phone_number=contact.phone_number,
            company_id=contact.company_id,
        )

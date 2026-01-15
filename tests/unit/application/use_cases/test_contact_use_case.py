import pytest

from src.application.use_cases.contact_use_cases import (
    CreateContactUseCase,
    DeleteContactUseCase,
    GetContactUseCase,
    UpdateContactUseCase,
)
from src.domain.errors import ContactNotFoundError
from src.helpers.helpers import generate_uuid4


def test_create_contact_use_case(contact_repository):
    # Arrange
    use_case = CreateContactUseCase(contact_repository=contact_repository)

    # Act
    contact = use_case.execute(
        name="Contact Name",
        phone_number="+558899034444",
        company_id=generate_uuid4(),
        email="contact@test.com",
    )

    # Assert
    assert contact_repository.get_by_id(contact.id)


def test_get_contact_use_case(contact_factory, contact_repository):
    # Arrange
    contact_1 = contact_factory(name="Contact 1", phone_number="5588999034444")
    contact_2 = contact_factory(name="Contact 2", phone_number="5588999034445")
    contact_repository.save(contact_1)
    contact_repository.save(contact_2)
    use_case = GetContactUseCase(contact_repository=contact_repository)

    # Act
    fetched_contact = use_case.execute(contact_id=contact_1.id)

    # Assert
    assert fetched_contact.name == contact_1.name
    assert fetched_contact.phone_number == contact_1.phone_number


def test_update_contact_use_case_existing_contact(contact, contact_repository):
    # Arrange
    use_case = UpdateContactUseCase(contact_repository=contact_repository)

    # Act
    new_name = "New Name"
    contact = use_case.execute(
        contact_id=contact.id,
        name=new_name,
        phone_number=contact.phone_number,
        company_id=contact.company_id,
        email=contact.email,
    )

    # Assert
    assert contact.name == new_name


def test_update_contact_use_case_non_existing_contact(contact_repository):
    # Arrange
    use_case = UpdateContactUseCase(contact_repository=contact_repository)

    # Act/Assert
    with pytest.raises(ContactNotFoundError):
        use_case.execute(
            contact_id="contact.id",
            name="New Name",
            phone_number="contact.phone_number",
            company_id="contact.company_id",
            email="contact@test.com",
        )


def test_delete_contact_use_case(contact, contact_repository):
    # Arrange
    use_case = DeleteContactUseCase(contact_repository=contact_repository)

    # Act
    use_case.execute(contact.id)

    # Act/Assert
    with pytest.raises(ContactNotFoundError):
        contact_repository.get_by_id(contact.id)

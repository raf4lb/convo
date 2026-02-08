import pytest

from src.application.use_cases.contact_use_cases import (
    CreateContactUseCase,
    DeleteContactUseCase,
    GetCompanyContactsUseCase,
    GetContactUseCase,
    SearchContactsUseCase,
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


def test_get_company_contacts_use_case(contact, contact_repository):
    # Arrange
    company_id = contact.company_id
    use_case = GetCompanyContactsUseCase(contact_repository=contact_repository)

    # Act
    contacts = use_case.execute(company_id=company_id)

    # Assert
    assert len(contacts) >= 1
    assert any(c.id == contact.id for c in contacts)
    assert all(c.company_id == company_id for c in contacts)


def test_search_contacts_use_case(contact_factory, contact_repository, company):
    # Arrange
    contact_factory(
        name="John Doe",
        phone_number="123456789",
        email="john@example.com",
        company_id=company.id,
    )
    contact_factory(
        name="Jane Smith",
        phone_number="987654321",
        email="jane@example.com",
        company_id=company.id,
    )

    contact_factory(
        name="Alice Brown",
        phone_number="555555555",
        email="alice@other.com",
        company_id=company.id,
    )
    # Different company
    contact_factory(
        name="John Other",
        phone_number="111111111",
        company_id="other_company",
    )

    use_case = SearchContactsUseCase(contact_repository=contact_repository)

    # Act - Search by name (case-insensitive)
    results_name = use_case.execute(company_id=company.id, query="JOHN")

    # Act - Search by phone
    results_phone = use_case.execute(company_id=company.id, query="9876")

    # Act - Search by email
    results_email = use_case.execute(company_id=company.id, query="EXAMPLE")

    # Assert
    assert len(results_name) == 1
    assert results_name[0].name == "John Doe"

    assert len(results_phone) == 1
    assert results_phone[0].name == "Jane Smith"

    assert len(results_email) == 2
    assert any(c.name == "John Doe" for c in results_email)
    assert any(c.name == "Jane Smith" for c in results_email)

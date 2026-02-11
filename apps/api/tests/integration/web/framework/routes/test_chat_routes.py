import pytest

from src.web.http_types import StatusCodes


def test_list_company_chats_endpoint(
    client, company_factory, chat_repository, chat_factory
):
    # Arrange
    client.app.state.chat_repository = chat_repository
    company_1 = company_factory()
    company_2 = company_factory()
    chats_1 = [chat_factory(company_id=company_1.id) for _ in range(3)]
    chats_2 = [chat_factory(company_id=company_2.id) for _ in range(2)]

    # Act
    response_1 = client.get(f"/chats/?company_id={company_1.id}")
    response_2 = client.get(f"/chats/?company_id={company_2.id}")

    # Assert
    assert len(response_1.json().get("results")) == len(chats_1)
    assert len(response_2.json().get("results")) == len(chats_2)


@pytest.mark.integration
def test_mark_chat_as_read_endpoint(
    client,
    chat,
    message_factory,
    message_repository,
):
    # Arrange - Add unread messages to the chat
    client.app.state.message_repository = message_repository
    message_1 = message_factory(chat_id=chat.id, read=False)
    message_2 = message_factory(chat_id=chat.id, read=False)

    # Verify messages start as unread
    assert message_1.read is False
    assert message_2.read is False

    # Act
    response = client.patch(f"/chats/{chat.id}/read")

    # Assert
    assert response.status_code == StatusCodes.OK.value
    assert "updated_count" in response.json()
    assert response.json()["updated_count"] == 2

    # Verify messages are marked as read
    updated_message_1 = message_repository.get_by_id(message_1.id)
    updated_message_2 = message_repository.get_by_id(message_2.id)
    assert updated_message_1.read is True
    assert updated_message_2.read is True
    assert updated_message_1.updated_at is not None
    assert updated_message_2.updated_at is not None


@pytest.mark.integration
def test_mark_chat_as_read_endpoint_already_read(
    client,
    chat,
    message_factory,
    message_repository,
):
    # Arrange
    client.app.state.message_repository = message_repository
    message_factory(chat_id=chat.id, read=False)

    # Act - Call twice
    first_response = client.patch(f"/chats/{chat.id}/read")
    second_response = client.patch(f"/chats/{chat.id}/read")

    # Assert - Second call should return 0 (idempotent)
    assert first_response.status_code == StatusCodes.OK.value
    assert second_response.status_code == StatusCodes.OK.value
    assert first_response.json()["updated_count"] == 1
    assert second_response.json()["updated_count"] == 0


@pytest.mark.integration
def test_mark_chat_as_read_endpoint_nonexistent_chat(
    client,
    message_repository,
):
    # Arrange
    client.app.state.message_repository = message_repository

    # Act
    response = client.patch("/chats/nonexistent-id/read")

    # Assert - Should succeed with count 0
    assert response.status_code == StatusCodes.OK.value
    assert response.json()["updated_count"] == 0

from src.web.http_types import StatusCodes


def test_get_message_endpoint(
    client,
    message,
    message_repository,
):
    # Arrange
    client.app.state.message_repository = message_repository

    # Act
    response = client.get(f"/messages/{message.id}")

    # Assert
    assert response.status_code == StatusCodes.OK.value
    assert response.json().get("text") == message.text


def test_get_message_endpoint_not_found(
    client,
    message_repository,
):
    # Arrange
    client.app.state.message_repository = message_repository

    # Act
    response = client.get("/messages/invalid_id")

    # Assert
    assert response.status_code == StatusCodes.NOT_FOUND.value


def test_receive_message_endpoint(
    client,
    message,
    receiver_contact,
    message_repository,
    contact_repository,
    chat_repository,
):
    # Arrange
    client.app.state.message_repository = message_repository
    client.app.state.contact_repository = contact_repository
    client.app.state.chat_repository = chat_repository

    message_text = "Hello!"
    data = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "<WHATSAPP_BUSINESS_ACCOUNT_ID>",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": receiver_contact.phone_number,
                                "phone_number_id": "<BUSINESS_PHONE_NUMBER_ID>",
                            },
                            "contacts": [
                                {
                                    "profile": {"name": "Sender Name"},
                                    "wa_id": "5588999034445",
                                }
                            ],
                            "messages": [
                                {
                                    "from": "5588999034445",
                                    "id": "<WHATSAPP_MESSAGE_ID>",
                                    "timestamp": "1730558382",
                                    "text": {"body": message_text},
                                    "type": "text",
                                }
                            ],
                        },
                        "field": "messages",
                    }
                ],
            }
        ],
    }

    # Act
    response = client.post("/messages/receive", json=data)

    # Assert
    assert response.status_code == StatusCodes.CREATED.value
    received_message = message_repository.get_by_id(
        message_id=response.json().get("message_id")
    )
    assert received_message.text == message_text

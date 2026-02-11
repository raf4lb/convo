from src.web.http_types import StatusCodes


def test_verify_webhook_endpoint(client):
    # Arrange
    test_challenge = "1234"

    # Act
    response = client.get(
        "/webhook/",
        params={
            "hub.mode": "subscribe",
            "hub.verify_token": client.app.state.settings.WEBHOOK_VERIFY_TOKEN,
            "hub.challenge": test_challenge,
        },
    )

    # Assert
    assert response.status_code == StatusCodes.OK.value
    assert response.text == test_challenge


def test_verify_webhook_endpoint_invalid_verify_token(client):
    # Arrange
    test_challenge = "1234"

    # Act
    response = client.get(
        "/webhook/",
        params={
            "hub.mode": "subscribe",
            "hub.verify_token": "invalid",
            "hub.challenge": test_challenge,
        },
    )

    # Assert
    assert response.status_code == StatusCodes.FORBIDDEN.value


def test_receive_messages_webhook_endpoint(
    client, receiver_contact, contact_repository
):
    # Arrange
    client.app.state.contact_repository = contact_repository
    receiver_contact.phone_number = "15551581534"
    contact_repository.save(receiver_contact)
    fake_message = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "1567784987708786",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "15551581534",
                                "phone_number_id": "933457093189375",
                            },
                            "contacts": [
                                {
                                    "profile": {"name": "Rafael Albuquerque"},
                                    "wa_id": "558899034444",
                                }
                            ],
                            "messages": [
                                {
                                    "from": "558899034444",
                                    "id": "wamid.HBgMNTU4ODk5MDM0NDQ0FQIAEhgUM0I0REIxQjRFQ0I4MjdDQjJCRUIA",
                                    "timestamp": "1770814438",
                                    "text": {"body": "hi"},
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
    response = client.post("/webhook/", json=fake_message)

    # Assert
    assert response.status_code == StatusCodes.CREATED.value
    assert "message_id" in response.json()

from src.web.http_types import StatusCodes


def test_verify_webhook(client):
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


def test_verify_webhook_invalid_verify_token(client):
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


def test_receive_messages_webhook(client):
    # Arrange
    fake_message = {"message_id": "123", "text": "this is a fake message"}

    # Act
    response = client.post("/webhook/", json=fake_message)

    # Assert
    assert response.status_code == StatusCodes.OK.value
    assert response.json() == {"received": fake_message}

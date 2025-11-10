from src.web.controllers.http_types import StatusCodes
from src.web.framework.routes.message_routes import message_route_blueprint


def test_get_message(
    app,
    client,
    message,
    message_repository,
):
    # Arrange
    app.config["message_repository"] = message_repository
    app.register_blueprint(message_route_blueprint, url_prefix="/messages")

    # Act
    response = client.get(f"/messages/{message.id}")

    # Assert
    assert response.status_code == StatusCodes.OK.value
    assert response.json.get("text") == message.text


def test_message_not_found(
    app,
    client,
    message_repository,
):
    # Arrange
    app.config["message_repository"] = message_repository
    app.register_blueprint(message_route_blueprint, url_prefix="/messages")

    # Act
    response = client.get("/messages/invalid_id")

    # Assert
    assert response.status_code == StatusCodes.NOT_FOUND.value


def test_receive_message(
    app,
    client,
    message,
    message_repository,
    contact_repository,
    chat_repository,
):
    # Arrange
    app.config["message_repository"] = message_repository
    app.config["contact_repository"] = contact_repository
    app.config["chat_repository"] = chat_repository
    app.register_blueprint(message_route_blueprint, url_prefix="/messages")

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
                                "display_phone_number": "5588999034444",
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
        message_id=response.json.get("message_id")
    )
    assert received_message.text == message_text

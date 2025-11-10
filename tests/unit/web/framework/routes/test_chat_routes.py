from src.web.framework.routes.chat_routes import chat_route_blueprint


def test_list_company_chats(
    app, client, company_factory, chat_repository, chat_factory
):
    # Arrange
    app.config["chat_repository"] = chat_repository
    app.register_blueprint(chat_route_blueprint, url_prefix="/chats")
    company_1 = company_factory()
    company_2 = company_factory()
    chats_1 = [chat_factory(company_id=company_1.id) for _ in range(3)]
    chats_2 = [chat_factory(company_id=company_2.id) for _ in range(2)]

    # Act
    response_1 = client.get(f"/chats/?company_id={company_1.id}")
    response_2 = client.get(f"/chats/?company_id={company_2.id}")

    # Assert
    assert len(response_1.json.get("chats")) == len(chats_1)
    assert len(response_2.json.get("chats")) == len(chats_2)

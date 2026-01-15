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

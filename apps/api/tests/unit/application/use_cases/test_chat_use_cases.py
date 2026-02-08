from src.application.use_cases.chat_use_cases import ListChatsByCompanyUseCase
from src.helpers.helpers import generate_uuid4


def test_list_chats_by_company_use_case(chat_factory, chat_repository):
    # Arrage
    company_id_1 = generate_uuid4()
    company_id_2 = generate_uuid4()
    chat_1 = chat_factory(company_id=company_id_1)
    chat_repository.save(chat_1)
    chat_2 = chat_factory(company_id=company_id_1)
    chat_repository.save(chat_2)
    chat_3 = chat_factory(company_id=company_id_2)
    chat_repository.save(chat_3)

    use_case = ListChatsByCompanyUseCase(chat_repository=chat_repository)

    # Act
    chats_company_1 = use_case.execute(company_id=company_id_1)
    chats_company_2 = use_case.execute(company_id=company_id_2)

    # Assert
    assert len(chats_company_1) == 2
    assert len(chats_company_2) == 1

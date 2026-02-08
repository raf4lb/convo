from src.domain.entities.chat import Chat
from src.domain.errors import ChatNotFoundError
from src.domain.repositories.chat_repository import IChatRepository


class InMemoryChatRepository(IChatRepository):
    def __init__(self):
        self.chats = {}

    def save(self, chat: Chat) -> Chat:
        self.chats[chat.id] = chat
        return chat

    def get_by_id(self, chat_id: str) -> Chat:
        chat = self.chats.get(chat_id)
        if chat is None:
            raise ChatNotFoundError
        return chat

    def get_all(self) -> list[Chat]:
        return list(self.chats.values())

    def get_by_company_id(self, company_id: str) -> list[Chat]:
        return [chat for chat in self.chats.values() if chat.company_id == company_id]

    def delete(self, chat_id: str) -> None:
        self.get_by_id(chat_id=chat_id)
        self.chats.pop(chat_id)

    def get_company_chat_by_contact_id(self, company_id: str, contact_id: str) -> Chat:
        for chat in self.chats.values():
            if chat.company_id == company_id and chat.contact_id == contact_id:
                return chat
        raise ChatNotFoundError

import { ChatDTO, ContactDTO, MessageDTO, UserDTO } from "./ApiMappers";

import { Conversation, ConversationStatus } from "@/domain/entities/Conversation";
import { Message } from "@/domain/entities/Message";
import { AuthUser, UserRole } from "@/domain/entities/User";
import { IConversationRepository } from "@/domain/repositories/IConversationRepository";
import { HttpClient } from "@/infrastructure/http/HttpClient";

export class ApiConversationRepository implements IConversationRepository {
  private userCache: Map<string, UserDTO> = new Map();
  private contactCache: Map<string, ContactDTO> = new Map();

  constructor(private readonly client: HttpClient) {}

  private mapChatStatus(backendStatus: string): ConversationStatus {
    const mapping: Record<string, ConversationStatus> = {
      open: ConversationStatus.PENDING,
      pending: ConversationStatus.PENDING,
      replied: ConversationStatus.ACTIVE,
      closed: ConversationStatus.RESOLVED,
    };
    return mapping[backendStatus] || ConversationStatus.PENDING;
  }

  private formatTime(date: Date): string {
    const now = new Date();
    const diffInDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));

    if (diffInDays === 0) {
      return date.toLocaleTimeString("pt-BR", {
        hour: "2-digit",
        minute: "2-digit",
      });
    } else if (diffInDays === 1) {
      return "Ontem";
    } else if (diffInDays < 7) {
      return `${diffInDays} dias atrás`;
    } else {
      return date.toLocaleDateString("pt-BR", {
        day: "2-digit",
        month: "2-digit",
      });
    }
  }

  private async getContact(contactId: string): Promise<ContactDTO> {
    if (this.contactCache.has(contactId)) {
      return this.contactCache.get(contactId)!;
    }

    const contact = await this.client.get<ContactDTO>(`/contacts/${contactId}`);
    this.contactCache.set(contactId, contact);
    return contact;
  }

  private async getUser(userId: string): Promise<UserDTO | null> {
    if (this.userCache.has(userId)) {
      return this.userCache.get(userId)!;
    }

    try {
      const user = await this.client.get<UserDTO>(`/users/${userId}`);
      this.userCache.set(userId, user);
      return user;
    } catch (error) {
      return null;
    }
  }

  private async mapChatToConversation(
    chat: ChatDTO,
    lastMessageText?: string,
    unreadCount?: number,
  ): Promise<Conversation> {
    const contact = await this.getContact(chat.contact_id);
    const attendantName = chat.attached_user_id
      ? (await this.getUser(chat.attached_user_id))?.name || null
      : null;

    return {
      id: chat.id,
      companyId: chat.company_id,
      customerId: chat.contact_id,
      customerName: contact.name,
      customerPhone: contact.phone_number,
      lastMessage: lastMessageText || "",
      time: this.formatTime(new Date(chat.created_at)),
      unread: unreadCount || 0,
      assignedToUserId: chat.attached_user_id,
      assignedToUserName: attendantName,
      status: this.mapChatStatus(chat.status),
      createdAt: new Date(chat.created_at),
      updatedAt: chat.updated_at ? new Date(chat.updated_at) : new Date(chat.created_at),
    };
  }

  private mapMessageDTOToMessage(dto: MessageDTO, userMap: Map<string, string>): Message {
    const isFromCustomer = dto.sent_by_user_id === null;
    const attendantName = dto.sent_by_user_id ? userMap.get(dto.sent_by_user_id) : undefined;

    return {
      id: dto.id,
      text: dto.text,
      timestamp: new Date(dto.external_timestamp).toLocaleTimeString("pt-BR", {
        hour: "2-digit",
        minute: "2-digit",
      }),
      sender: isFromCustomer ? "customer" : "attendant",
      attendantName,
    };
  }

  async getAll(companyId: string): Promise<Conversation[]> {
    const response = await this.client.get<{ results: ChatDTO[] }>(
      `/chats?company_id=${companyId}`,
    );

    const conversations: Conversation[] = [];
    for (const chat of response.results) {
      try {
        const messages = await this.client.get<{ results: MessageDTO[] }>(
          `/chats/${chat.id}/messages`,
        );
        const lastMessage =
          messages.results.length > 0 ? messages.results[messages.results.length - 1].text : "";
        const unreadCount = messages.results.filter(
          (m) => !m.read && m.sent_by_user_id === null,
        ).length;

        const conversation = await this.mapChatToConversation(chat, lastMessage, unreadCount);
        conversations.push(conversation);
      } catch {
        const conversation = await this.mapChatToConversation(chat);
        conversations.push(conversation);
      }
    }

    return conversations;
  }

  async getById(companyId: string, id: string): Promise<Conversation | null> {
    try {
      const chat = await this.client.get<ChatDTO>(`/chats/${id}`);
      if (chat.company_id !== companyId) {
        return null;
      }

      const messages = await this.client.get<{ results: MessageDTO[] }>(`/chats/${id}/messages`);
      const lastMessage =
        messages.results.length > 0 ? messages.results[messages.results.length - 1].text : "";
      const unreadCount = messages.results.filter(
        (m) => !m.read && m.sent_by_user_id === null,
      ).length;

      return await this.mapChatToConversation(chat, lastMessage, unreadCount);
    } catch (error) {
      return null;
    }
  }

  async getByAttendant(user: AuthUser): Promise<Conversation[]> {
    let chats: ChatDTO[];

    if (user.role === UserRole.ATTENDANT) {
      const response = await this.client.get<{ results: ChatDTO[] }>(
        `/chats/by-attendant?company_id=${user.companyId}&attendant_id=${user.id}`,
      );
      chats = response.results;
    } else {
      const response = await this.client.get<{ results: ChatDTO[] }>(
        `/chats?company_id=${user.companyId}`,
      );
      chats = response.results;
    }

    const conversations: Conversation[] = [];
    for (const chat of chats) {
      try {
        const messages = await this.client.get<{ results: MessageDTO[] }>(
          `/chats/${chat.id}/messages`,
        );
        const lastMessage =
          messages.results.length > 0 ? messages.results[messages.results.length - 1].text : "";
        const unreadCount = messages.results.filter(
          (m) => !m.read && m.sent_by_user_id === null,
        ).length;

        const conversation = await this.mapChatToConversation(chat, lastMessage, unreadCount);
        conversations.push(conversation);
      } catch {
        const conversation = await this.mapChatToConversation(chat);
        conversations.push(conversation);
      }
    }

    return conversations;
  }

  async getMessages(conversationId: string): Promise<Message[]> {
    const response = await this.client.get<{ results: MessageDTO[] }>(
      `/chats/${conversationId}/messages`,
    );

    const userIds = new Set(
      response.results.map((m) => m.sent_by_user_id).filter((id): id is string => id !== null),
    );

    const userMap = new Map<string, string>();
    for (const userId of userIds) {
      const user = await this.getUser(userId);
      if (user) {
        userMap.set(userId, user.name);
      }
    }

    return response.results.map((dto) => this.mapMessageDTOToMessage(dto, userMap));
  }

  async assignAttendant(
    conversationId: string,
    userId: string | null,
    userName: string | null,
  ): Promise<void> {
    await this.client.patch(`/chats/${conversationId}/assign`, {
      attendant_id: userId,
    });

    if (userId && userName) {
      this.userCache.set(userId, { name: userName } as UserDTO);
    }
  }

  async sendMessage(conversationId: string, message: Omit<Message, "id">): Promise<Message> {
    const response = await this.client.post<MessageDTO>(`/chats/${conversationId}/messages`, {
      text: message.text,
      sent_by_user_id: "current_user_id", // TODO: get from auth context
    });

    const userMap = new Map<string, string>();
    if (response.sent_by_user_id && message.attendantName) {
      userMap.set(response.sent_by_user_id, message.attendantName);
    }

    return this.mapMessageDTOToMessage(response, userMap);
  }

  async receiveMessage(conversationId: string, message: Message): Promise<Message> {
    // This is a client-side operation for WebSocket messages
    // No API call needed, just return the message
    return Promise.resolve(message);
  }

  async search(companyId: string, query: string): Promise<Conversation[]> {
    const response = await this.client.get<{ results: ChatDTO[] }>(
      `/chats/search?company_id=${companyId}&query=${encodeURIComponent(query)}`,
    );

    const conversations: Conversation[] = [];
    for (const chat of response.results) {
      try {
        const messages = await this.client.get<{ results: MessageDTO[] }>(
          `/chats/${chat.id}/messages`,
        );
        const lastMessage =
          messages.results.length > 0 ? messages.results[messages.results.length - 1].text : "";
        const unreadCount = messages.results.filter(
          (m) => !m.read && m.sent_by_user_id === null,
        ).length;

        const conversation = await this.mapChatToConversation(chat, lastMessage, unreadCount);
        conversations.push(conversation);
      } catch {
        const conversation = await this.mapChatToConversation(chat);
        conversations.push(conversation);
      }
    }

    return conversations;
  }

  async getUnassigned(companyId: string): Promise<Conversation[]> {
    const response = await this.client.get<{ results: ChatDTO[] }>(
      `/chats/unassigned?company_id=${companyId}`,
    );

    const conversations: Conversation[] = [];
    for (const chat of response.results) {
      try {
        const messages = await this.client.get<{ results: MessageDTO[] }>(
          `/chats/${chat.id}/messages`,
        );
        const lastMessage =
          messages.results.length > 0 ? messages.results[messages.results.length - 1].text : "";
        const unreadCount = messages.results.filter(
          (m) => !m.read && m.sent_by_user_id === null,
        ).length;

        const conversation = await this.mapChatToConversation(chat, lastMessage, unreadCount);
        conversations.push(conversation);
      } catch {
        const conversation = await this.mapChatToConversation(chat);
        conversations.push(conversation);
      }
    }

    return conversations;
  }
}

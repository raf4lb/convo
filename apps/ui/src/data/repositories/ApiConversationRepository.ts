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

    const res = await this.client.get(`/contacts/${contactId}`);
    const contact = res.data as ContactDTO;
    this.contactCache.set(contactId, contact);
    return contact;
  }

  private async getUser(userId: string): Promise<UserDTO | null> {
    if (this.userCache.has(userId)) {
      return this.userCache.get(userId)!;
    }

    try {
      const res = await this.client.get(`/users/${userId}`);
      const user = res.data as UserDTO;
      this.userCache.set(userId, user);
      return user;
    } catch {
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
      customerName: contact.name || "Unknown",
      customerPhone: contact.phone_number || "",
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
    const res = await this.client.get(`/chats`, { query: { company_id: companyId } });
    const chats = (res.data as any).results as ChatDTO[];

    // Fetch all messages in parallel for better performance
    const messagePromises = chats.map((chat) =>
      this.client
        .get(`/chats/${chat.id}/messages`)
        .then((r) => (r.data as any).results as MessageDTO[])
        .catch(() => [] as MessageDTO[]),
    );

    const allMessages = await Promise.all(messagePromises);

    // Create a map of chat_id to messages
    const messagesMap = new Map<string, MessageDTO[]>();
    chats.forEach((chat, index) => {
      messagesMap.set(chat.id, allMessages[index] || []);
    });

    // Fetch all unique contacts in parallel
    const uniqueContactIds = [...new Set(chats.map((c) => c.contact_id))];
    const contactPromises = uniqueContactIds.map((id) => this.getContact(id).catch(() => null));
    const contacts = await Promise.all(contactPromises);
    const contactMap = new Map<string, ContactDTO>();
    uniqueContactIds.forEach((id, index) => {
      if (contacts[index]) {
        contactMap.set(id, contacts[index]!);
      }
    });

    // Fetch all unique users in parallel
    const uniqueUserIds = [
      ...new Set(chats.map((c) => c.attached_user_id).filter((id): id is string => id !== null)),
    ];
    const userPromises = uniqueUserIds.map((id) => this.getUser(id).catch(() => null));
    const users = await Promise.all(userPromises);
    const userMap = new Map<string, UserDTO>();
    uniqueUserIds.forEach((id, index) => {
      if (users[index]) {
        userMap.set(id, users[index]!);
      }
    });

    // Build conversations
    const conversations: Conversation[] = [];
    for (const chat of chats) {
      const contact = contactMap.get(chat.contact_id);
      if (!contact) continue; // Skip if contact not found

      const messages = messagesMap.get(chat.id) || [];
      const lastMessage = messages.length > 0 ? messages[messages.length - 1].text : "";
      const unreadCount = messages.filter((m) => !m.read && m.sent_by_user_id === null).length;
      const attendantName = chat.attached_user_id
        ? userMap.get(chat.attached_user_id)?.name || null
        : null;

      conversations.push({
        id: chat.id,
        companyId: chat.company_id,
        customerId: chat.contact_id,
        customerName: contact.name,
        customerPhone: contact.phone_number,
        lastMessage: lastMessage,
        time: this.formatTime(new Date(chat.created_at)),
        unread: unreadCount,
        assignedToUserId: chat.attached_user_id,
        assignedToUserName: attendantName,
        status: this.mapChatStatus(chat.status),
        createdAt: new Date(chat.created_at),
        updatedAt: chat.updated_at ? new Date(chat.updated_at) : new Date(chat.created_at),
      });
    }

    return conversations;
  }

  async getById(companyId: string, id: string): Promise<Conversation | null> {
    try {
      const chatRes = await this.client.get(`/chats/${id}`);
      const chat = chatRes.data as ChatDTO;
      if (chat.company_id !== companyId) {
        return null;
      }

      const messagesRes = await this.client.get(`/chats/${id}/messages`);
      const messages = ((messagesRes.data as any).results as MessageDTO[]) || [];
      const lastMessage = messages.length > 0 ? messages[messages.length - 1].text : "";
      const unreadCount = messages.filter((m) => !m.read && m.sent_by_user_id === null).length;

      return await this.mapChatToConversation(chat, lastMessage, unreadCount);
    } catch {
      return null;
    }
  }

  async getByAttendant(user: AuthUser): Promise<Conversation[]> {
    let res;

    if (user.role === UserRole.ATTENDANT) {
      res = await this.client.get(`/chats/by-attendant`, {
        query: { company_id: user.companyId, attendant_id: user.id },
      });
    } else {
      res = await this.client.get(`/chats`, { query: { company_id: user.companyId } });
    }

    const chats = ((res.data as any).results as ChatDTO[]) || [];
    return await this.buildConversationsFromChats(chats);
  }

  private async buildConversationsFromChats(chats: ChatDTO[]): Promise<Conversation[]> {
    // Fetch all messages in parallel
    const messagePromises = chats.map((chat) =>
      this.client
        .get(`/chats/${chat.id}/messages`)
        .then((r) => ((r.data as any).results as MessageDTO[]) || [])
        .catch(() => [] as MessageDTO[]),
    );
    const allMessages = await Promise.all(messagePromises);

    // Fetch all unique contacts in parallel
    const uniqueContactIds = [...new Set(chats.map((c) => c.contact_id))];
    const contacts = await Promise.all(
      uniqueContactIds.map((id) => this.getContact(id).catch(() => null)),
    );
    const contactMap = new Map<string, ContactDTO>();
    uniqueContactIds.forEach((id, index) => {
      if (contacts[index]) contactMap.set(id, contacts[index]!);
    });

    // Fetch all unique users in parallel
    const uniqueUserIds = [
      ...new Set(chats.map((c) => c.attached_user_id).filter((id): id is string => id !== null)),
    ];
    const users = await Promise.all(uniqueUserIds.map((id) => this.getUser(id).catch(() => null)));
    const userMap = new Map<string, UserDTO>();
    uniqueUserIds.forEach((id, index) => {
      if (users[index]) userMap.set(id, users[index]!);
    });

    // Build conversations
    const conversations: Conversation[] = [];
    for (let i = 0; i < chats.length; i++) {
      const chat = chats[i];
      const contact = contactMap.get(chat.contact_id);
      if (!contact || !contact.name) continue; // Skip if contact not found or has no name

      const messages = allMessages[i] || [];
      const lastMessage = messages.length > 0 ? messages[messages.length - 1].text : "";
      const unreadCount = messages.filter((m) => !m.read && m.sent_by_user_id === null).length;
      const attendantName = chat.attached_user_id
        ? userMap.get(chat.attached_user_id)?.name || null
        : null;

      conversations.push({
        id: chat.id,
        companyId: chat.company_id,
        customerId: chat.contact_id,
        customerName: contact.name,
        customerPhone: contact.phone_number || "",
        lastMessage: lastMessage || "",
        time: this.formatTime(new Date(chat.created_at)),
        unread: unreadCount,
        assignedToUserId: chat.attached_user_id,
        assignedToUserName: attendantName,
        status: this.mapChatStatus(chat.status),
        createdAt: new Date(chat.created_at),
        updatedAt: chat.updated_at ? new Date(chat.updated_at) : new Date(chat.created_at),
      });
    }

    return conversations;
  }

  async getMessages(conversationId: string): Promise<Message[]> {
    const res = await this.client.get(`/chats/${conversationId}/messages`);
    const messages = ((res.data as any).results as MessageDTO[]) || [];

    const userIds = new Set(
      messages.map((m) => m.sent_by_user_id).filter((id): id is string => id !== null),
    );

    const userMap = new Map<string, string>();
    for (const userId of userIds) {
      const user = await this.getUser(userId);
      if (user) {
        userMap.set(userId, user.name);
      }
    }

    return messages.map((dto) => this.mapMessageDTOToMessage(dto, userMap));
  }

  async assignAttendant(
    conversationId: string,
    userId: string | null,
    userName: string | null,
  ): Promise<void> {
    await this.client.patch(`/chats/${conversationId}/assign`, {
      body: { attendant_id: userId },
    });

    if (userId && userName) {
      this.userCache.set(userId, { name: userName } as UserDTO);
    }
  }

  async sendMessage(conversationId: string, message: Omit<Message, "id">): Promise<Message> {
    const res = await this.client.post(`/chats/${conversationId}/messages`, {
      body: {
        text: message.text,
        sent_by_user_id: "current_user_id", // TODO: get from auth context
      },
    });
    const msgDTO = res.data as MessageDTO;

    const userMap = new Map<string, string>();
    if (msgDTO.sent_by_user_id && message.attendantName) {
      userMap.set(msgDTO.sent_by_user_id, message.attendantName);
    }

    return this.mapMessageDTOToMessage(msgDTO, userMap);
  }

  async receiveMessage(conversationId: string, message: Message): Promise<Message> {
    // This is a client-side operation for WebSocket messages
    // No API call needed, just return the message
    return Promise.resolve(message);
  }

  async search(companyId: string, query: string): Promise<Conversation[]> {
    const res = await this.client.get(`/chats/search`, {
      query: { company_id: companyId, query },
    });
    const chats = ((res.data as any).results as ChatDTO[]) || [];
    return await this.buildConversationsFromChats(chats);
  }

  async getUnassigned(companyId: string): Promise<Conversation[]> {
    const res = await this.client.get(`/chats/unassigned`, {
      query: { company_id: companyId },
    });
    const chats = ((res.data as any).results as ChatDTO[]) || [];
    return await this.buildConversationsFromChats(chats);
  }

  async getPending(companyId: string): Promise<Conversation[]> {
    const res = await this.client.get(`/chats/pending`, {
      query: { company_id: companyId },
    });
    const chats = ((res.data as any).results as ChatDTO[]) || [];
    const conversations = await this.buildConversationsFromChats(chats);
    // Client-side filter for unread > 0 (final PENDING requirement)
    return conversations.filter((conv) => conv.unread > 0);
  }

  async getResolved(companyId: string): Promise<Conversation[]> {
    const res = await this.client.get(`/chats/resolved`, {
      query: { company_id: companyId },
    });
    const chats = ((res.data as any).results as ChatDTO[]) || [];
    return await this.buildConversationsFromChats(chats);
  }

  async markChatAsRead(conversationId: string): Promise<void> {
    await this.client.patch(`/chats/${conversationId}/read`);
  }
}

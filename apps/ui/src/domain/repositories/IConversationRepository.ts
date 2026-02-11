import { Conversation } from "../entities/Conversation";
import { Message } from "../entities/Message";
import { AuthUser } from "../entities/User";

export interface IConversationRepository {
  getAll(companyId: string): Promise<Conversation[]>;
  getById(companyId: string, id: string): Promise<Conversation | null>;
  getByAttendant(user: AuthUser): Promise<Conversation[]>;
  getMessages(conversationId: string): Promise<Message[]>;
  assignAttendant(
    conversationId: string,
    userId: string | null,
    userName: string | null,
  ): Promise<void>;
  sendMessage(conversationId: string, message: Omit<Message, "id">): Promise<Message>;
  receiveMessage(conversationId: string, message: Message): Promise<Message>;
  search(companyId: string, query: string): Promise<Conversation[]>;
  getUnassigned(companyId: string): Promise<Conversation[]>;
  getPending(companyId: string): Promise<Conversation[]>;
  getResolved(companyId: string): Promise<Conversation[]>;
}

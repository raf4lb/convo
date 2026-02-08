import { Conversation } from "../../entities/Conversation";
import { IConversationRepository } from "../../repositories/IConversationRepository";

export class SearchConversations {
  constructor(private conversationRepository: IConversationRepository) {}

  async execute(companyId: string, query: string): Promise<Conversation[]> {
    return await this.conversationRepository.search(companyId, query.trim());
  }
}

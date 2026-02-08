import { Message } from "../../entities/Message";
import { IConversationRepository } from "../../repositories/IConversationRepository";

export class GetConversationMessages {
  constructor(private conversationRepository: IConversationRepository) {}

  async execute(conversationId: string): Promise<Message[]> {
    return await this.conversationRepository.getMessages(conversationId);
  }
}

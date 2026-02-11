import { ConversationReadEvent } from "../../events/ConversationReadEvent";
import { IEventBus } from "../../ports/IEventBus";
import { IConversationRepository } from "../../repositories/IConversationRepository";

export class MarkConversationAsRead {
  constructor(
    private conversationRepository: IConversationRepository,
    private readonly eventBus: IEventBus,
  ) {}

  async execute(conversationId: string): Promise<void> {
    await this.conversationRepository.markChatAsRead(conversationId);
    const event = new ConversationReadEvent({
      conversationId,
    });
    await this.eventBus.publish(event);
  }
}

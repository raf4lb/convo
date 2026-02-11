import { ConversationAssignedEvent } from "../../events/ConversationAssignedEvent";
import { IEventBus } from "../../ports/IEventBus";
import { IConversationRepository } from "../../repositories/IConversationRepository";

export class AssignConversationToAttendant {
  constructor(
    private readonly conversationRepository: IConversationRepository,
    private readonly eventBus: IEventBus,
  ) {}

  async execute(
    conversationId: string,
    userId: string | null,
    userName: string | null,
  ): Promise<void> {
    await this.conversationRepository.assignAttendant(conversationId, userId, userName);
    const event = new ConversationAssignedEvent({ conversationId, userId, userName });
    await this.eventBus.publish(event);
  }
}

import { EventType, IDomainEvent } from "./IDomainEvent";

export type ConversationAssignedPayload = {
  conversationId: string;
  userId: string | null;
  userName: string | null;
  source?: string;
};

export class ConversationAssignedEvent implements IDomainEvent<ConversationAssignedPayload> {
  public readonly name = EventType.CONVERSATION_ASSIGNED;
  public readonly occurredAt: Date;
  constructor(public readonly payload: ConversationAssignedPayload) {
    this.occurredAt = new Date();
  }
}

import { EventType, IDomainEvent } from "./IDomainEvent";

export type ConversationReadPayload = {
  conversationId: string;
};

export class ConversationReadEvent implements IDomainEvent<ConversationReadPayload> {
  public readonly name = EventType.CONVERSATION_READ;
  public readonly occurredAt: Date;
  constructor(public readonly payload: ConversationReadPayload) {
    this.occurredAt = new Date();
  }
}

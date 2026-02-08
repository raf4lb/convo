import { Message } from "../entities/Message";

import { EventType, IDomainEvent } from "./IDomainEvent";

export type MessageSentPayload = {
  conversationId: string;
  message: Message;
  source?: string;
};

export class MessageSentEvent implements IDomainEvent<MessageSentPayload> {
  public readonly name = EventType.MESSAGE_SENT;
  public readonly occurredAt: Date;
  constructor(public readonly payload: MessageSentPayload) {
    this.occurredAt = new Date();
  }
}

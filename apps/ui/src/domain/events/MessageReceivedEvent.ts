import { Message } from "../entities/Message";

import { EventType, IDomainEvent } from "./IDomainEvent";

export type MessageReceivedPayload = {
  conversationId: string;
  message: Message;
  source?: string;
};

export class MessageReceivedEvent implements IDomainEvent<MessageReceivedPayload> {
  public readonly name = EventType.MESSAGE_RECEIVED;
  public readonly occurredAt: Date;
  constructor(public readonly payload: MessageReceivedPayload) {
    this.occurredAt = new Date();
  }
}

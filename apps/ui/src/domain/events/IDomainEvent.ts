export enum EventType {
  MESSAGE_SENT = "MessageSent",
  MESSAGE_RECEIVED = "MessageReceived",
  CONVERSATION_ASSIGNED = "ConversationAssigned",
}

export interface IDomainEvent<T = any> {
  readonly name: EventType;
  readonly occurredAt: Date;
  readonly payload: T;
}

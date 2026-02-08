import { IDomainEvent } from "../events/IDomainEvent";

export type EventHandler<T extends IDomainEvent = IDomainEvent> = (
  event: T,
) => Promise<void> | void;

/**
 * Port (interface) for publishing events and subscribing handlers.
 * Use cases and domain depend on this interface.
 */
export interface IEventBus {
  publish<T extends IDomainEvent>(event: T): Promise<void>;
  subscribe<T extends IDomainEvent>(eventName: string, handler: EventHandler<T>): () => void; // returns unsubscribe
}

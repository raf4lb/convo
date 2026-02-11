import { IDomainEvent } from "@/domain/events/IDomainEvent";
import { EventHandler, IEventBus } from "@/domain/ports/IEventBus";

/**
 * Implementação simples de EventBus em memória.
 * - Suporta múltiplos handlers por eventName.
 * - Ao publicar, todos os handlers são executados concorrentemente (Promise.allSettled).
 */
export class InMemoryEventBus implements IEventBus {
  private handlers = new Map<string, Set<EventHandler<any>>>();

  async publish<T extends IDomainEvent>(event: T): Promise<void> {
    const set = this.handlers.get(event.name);
    if (!set || set.size === 0) return;

    // run all handlers concurrently and wait.
    const promises = Array.from(set).map((h) =>
      Promise.resolve()
        .then(() => h(event))
        .catch((err) => {
          console.error(`[InMemoryEventBus] handler erro em event ${event.name}`, err);
        }),
    );

    await Promise.allSettled(promises);
  }

  subscribe<T extends IDomainEvent>(eventName: string, handler: EventHandler<T>): () => void {
    const set = this.handlers.get(eventName) ?? new Set<EventHandler<any>>();
    set.add(handler as EventHandler<any>);
    this.handlers.set(eventName, set);

    return () => {
      set.delete(handler as EventHandler<any>);
      if (set.size === 0) this.handlers.delete(eventName);
    };
  }
}

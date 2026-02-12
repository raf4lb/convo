import { Message } from "../../entities/Message";
import { MessageSentEvent } from "../../events/MessageSentEvent";
import { IEventBus } from "../../ports/IEventBus";
import { IConversationRepository } from "../../repositories/IConversationRepository";

export class SendMessage {
  constructor(
    private conversationRepository: IConversationRepository,
    private readonly eventBus: IEventBus,
  ) {}

  async execute(
    conversationId: string,
    message: Omit<Message, "id">,
    userId: string,
  ): Promise<Message> {
    const newMessage = await this.conversationRepository.sendMessage(
      conversationId,
      message,
      userId,
    );
    const event = new MessageSentEvent({
      conversationId,
      message: newMessage,
      source: "payload.source",
    });
    await this.eventBus.publish(event);
    return newMessage;
  }
}

import { Message } from "../../entities/Message";
import { MessageReceivedEvent } from "../../events/MessageReceivedEvent";
import { IEventBus } from "../../ports/IEventBus";
import { IConversationRepository } from "../../repositories/IConversationRepository";

export type Subscriber = (messages: Message[]) => void;

export class ReceiveMessage {
  constructor(
    private readonly conversationRepository: IConversationRepository,
    private readonly eventBus: IEventBus,
  ) {}

  async execute(conversationId: string, message: Message): Promise<Message> {
    const newMessage = await this.conversationRepository.receiveMessage(conversationId, message);
    const event = new MessageReceivedEvent({ conversationId, message, source: "payload.source" });
    await this.eventBus.publish(event);
    return newMessage;
  }
}

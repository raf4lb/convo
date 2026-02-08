import { receiveMessageUseCase } from "../di/container";

export async function onMessageReceivedHandler(data: any): Promise<void> {
  const { conversationId, ...message } = data;
  await receiveMessageUseCase.execute(conversationId, message);
}

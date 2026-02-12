import { receiveMessageUseCase } from "../di/container";

import { formatRelativeTime } from "@/utils/dateTime";

export async function onMessageReceivedHandler(data: any): Promise<void> {
  const { conversationId, ...message } = data;

  // Format ISO timestamp to relative time using browser's local timezone
  if (message.timestamp && typeof message.timestamp === "string") {
    message.timestamp = formatRelativeTime(message.timestamp);
  }

  await receiveMessageUseCase.execute(conversationId, message);
}

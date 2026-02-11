import { useCallback, useEffect, useState } from "react";

import { Message } from "@/domain/entities/Message";
import { EventType } from "@/domain/events/IDomainEvent";
import { MessageReceivedEvent } from "@/domain/events/MessageReceivedEvent";
import { MessageSentEvent } from "@/domain/events/MessageSentEvent";
import { IEventBus } from "@/domain/ports/IEventBus";
import {
  getConversationMessagesUseCase,
  sendMessageUseCase,
} from "@/infrastructure/di/container";

export function useConversationMessages(conversationId: string | null, eventBus: IEventBus) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [isSendingMessage, setIsSendingMessage] = useState(false);

  const loadMessages = useCallback(async () => {
    if (!conversationId) return;

    try {
      setLoading(true);
      const data = await getConversationMessagesUseCase.execute(conversationId);
      setMessages(data);
      setError(null);
    } catch (err) {
      setError(err as Error);
    } finally {
      setLoading(false);
    }
  }, [conversationId]);

  const onMessageSent = useCallback(
    (messageConversationId: string, message: Message) => {
      if (messageConversationId != conversationId) return;
      setMessages((prev) => [...prev, message]);
    },
    [conversationId],
  );

  const onMessageReceived = useCallback(
    (messageConversationId: string, message: Message) => {
      if (messageConversationId != conversationId) return;
      setMessages((prev) => [...prev, message]);
    },
    [conversationId],
  );

  useEffect(() => {
    if (conversationId) {
      loadMessages();
    }

    const unsubscribeMessageSentEvent = eventBus.subscribe<MessageSentEvent>(
      EventType.MESSAGE_SENT,
      (event) => {
        if (event.payload.conversationId != conversationId) return;
        onMessageSent(event.payload.conversationId, event.payload.message);
      },
    );

    const unsubscribeMessageReceivedEvent = eventBus.subscribe<MessageReceivedEvent>(
      EventType.MESSAGE_RECEIVED,
      (event) => {
        if (event.payload.conversationId != conversationId) return;
        onMessageReceived(event.payload.conversationId, event.payload.message);
      },
    );

    return () => {
      unsubscribeMessageSentEvent();
      unsubscribeMessageReceivedEvent();
    };
  }, [conversationId, loadMessages, eventBus, onMessageSent, onMessageReceived]);

  const sendMessage = async (text: string, attendantName: string) => {
    if (!conversationId) return;
    try {
      setIsSendingMessage(true);
      await sendMessageUseCase.execute(conversationId, {
        text: text,
        timestamp: new Date().toISOString(),
        sender: "attendant",
        attendantName: attendantName,
      });
      setError(null);
    } catch (err) {
      setError(err as Error);
    } finally {
      setIsSendingMessage(false);
    }
  };

  return {
    messages,
    loading,
    error,
    reload: loadMessages,
    isSendingMessage,
    sendMessage,
  };
}

import { Dispatch, SetStateAction, useCallback, useEffect, useState } from "react";

import { useAuth } from "./useAuth";

import { Conversation } from "@/domain/entities/Conversation";
import {
  ConversationAssignedEvent,
  ConversationAssignedPayload,
} from "@/domain/events/ConversationAssignedEvent";
import { EventType } from "@/domain/events/IDomainEvent";
import { MessageReceivedEvent, MessageReceivedPayload } from "@/domain/events/MessageReceivedEvent";
import { MessageSentEvent, MessageSentPayload } from "@/domain/events/MessageSentEvent";
import { IEventBus } from "@/domain/ports/IEventBus";
import {
  getConversationsUseCase,
  getConversationUseCase,
  searchConversationsUseCase,
} from "@/infrastructure/di/container";

export interface ConversationsHook {
  conversations: Conversation[];
  setConversations: Dispatch<SetStateAction<Conversation[]>>;
  loading: boolean;
  error: Error | null;
  reload: () => Promise<void>;
  search: (query: string) => Promise<void>;
}

export function useConversations(eventBus: IEventBus) {
  const { session } = useAuth();
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const loadConversations = useCallback(async () => {
    if (!session) throw new Error("No session");

    try {
      setLoading(true);
      const data = await getConversationsUseCase.execute(session.user);
      setConversations(data);
      setError(null);
    } catch (err) {
      setError(err as Error);
    } finally {
      setLoading(false);
    }
  }, [session]);

  const onMessageSent = useCallback(
    async (payload: MessageSentPayload) => {
      if (!session) return;
      const updatedConvo = await getConversationUseCase.execute(
        payload.conversationId,
        session.user,
      );
      if (!updatedConvo) return;
      setConversations((prev) =>
        prev.map((conv) => (conv.id === payload.conversationId ? updatedConvo : conv)),
      );
    },
    [session, setConversations],
  );

  const onMessageReceived = useCallback(
    async (payload: MessageReceivedPayload) => {
      if (!session) return;
      const updatedConvo = await getConversationUseCase.execute(
        payload.conversationId,
        session.user,
      );
      if (!updatedConvo) return;
      setConversations((prev) =>
        prev.map((conv) => (conv.id === payload.conversationId ? updatedConvo : conv)),
      );
    },
    [session, setConversations],
  );

  useEffect(() => {
    if (session) {
      loadConversations();

      const unsubscribeMessageSentEvent = eventBus.subscribe<MessageSentEvent>(
        EventType.MESSAGE_SENT,
        async (event) => {
          onMessageSent(event.payload);
        },
      );

      const unsubscribeMessageReceivedEvent = eventBus.subscribe<MessageReceivedEvent>(
        EventType.MESSAGE_RECEIVED,
        async (event) => {
          onMessageReceived(event.payload);
        },
      );

      const unsubscribeConversationAssignedEvent = eventBus.subscribe<ConversationAssignedEvent>(
        EventType.CONVERSATION_ASSIGNED,
        async (event) => {
          onConversationAssigned(event.payload);
        },
      );

      return () => {
        unsubscribeMessageSentEvent();
        unsubscribeMessageReceivedEvent();
        unsubscribeConversationAssignedEvent();
      };
    }
  }, [session, loadConversations, eventBus, onMessageReceived, onMessageSent]);

  const search = async (query: string) => {
    if (!session) throw new Error("No session");

    try {
      setLoading(true);
      const data = await searchConversationsUseCase.execute(session.company.id, query);
      setConversations(data);
      setError(null);
    } catch (err) {
      setError(err as Error);
    } finally {
      setLoading(false);
    }
  };

  const onConversationAssigned = (payload: ConversationAssignedPayload) => {
    setConversations((prev) =>
      prev.map((conv) =>
        conv.id === payload.conversationId
          ? { ...conv, assignedToUserId: payload.userId, assignedToUserName: payload.userName }
          : conv,
      ),
    );
  };

  return {
    conversations,
    setConversations,
    loading,
    error,
    reload: loadConversations,
    search,
  };
}

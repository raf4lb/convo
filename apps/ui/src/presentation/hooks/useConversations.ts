import { Dispatch, SetStateAction, useCallback, useEffect, useState } from "react";

import { useAuth } from "./useAuth";

import { Conversation } from "@/domain/entities/Conversation";
import { ConversationAssignedEvent } from "@/domain/events/ConversationAssignedEvent";
import { ConversationReadEvent } from "@/domain/events/ConversationReadEvent";
import { EventType } from "@/domain/events/IDomainEvent";
import { MessageReceivedEvent } from "@/domain/events/MessageReceivedEvent";
import { MessageSentEvent } from "@/domain/events/MessageSentEvent";
import { IEventBus } from "@/domain/ports/IEventBus";
import {
  conversationRepository,
  getConversationsUseCase,
  getConversationUseCase,
  markConversationAsReadUseCase,
  searchConversationsUseCase,
} from "@/infrastructure/di/container";
import { TabType } from "@/presentation/constants/tabTypes";

export interface ConversationsHook {
  conversations: Conversation[];
  setConversations: Dispatch<SetStateAction<Conversation[]>>;
  loading: boolean;
  error: Error | null;
  reload: () => Promise<void>;
  search: (query: string) => Promise<void>;
}

export function useConversations(eventBus: IEventBus, filter?: TabType) {
  const { session } = useAuth();
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const loadConversations = useCallback(async () => {
    if (!session) throw new Error("No session");

    try {
      setLoading(true);
      let data: Conversation[];

      // Use filtered endpoints based on tab type
      if (filter === TabType.PENDING) {
        data = await conversationRepository.getPending(session.company.id);
      } else if (filter === TabType.RESOLVED) {
        data = await conversationRepository.getResolved(session.company.id);
      } else if (filter === TabType.UNASSIGNED) {
        data = await conversationRepository.getUnassigned(session.company.id);
      } else {
        // ALL tab - use existing logic with company settings check
        data = await getConversationsUseCase.execute(session.user);
      }

      setConversations(data);
      setError(null);
    } catch (err) {
      setError(err as Error);
    } finally {
      setLoading(false);
    }
  }, [session, filter]);

  useEffect(() => {
    if (session) {
      loadConversations();

      const unsubscribeMessageSentEvent = eventBus.subscribe<MessageSentEvent>(
        EventType.MESSAGE_SENT,
        async (event) => {
          if (!session) return;
          const updatedConvo = await getConversationUseCase.execute(
            event.payload.conversationId,
            session.user,
          );
          if (!updatedConvo) return;
          setConversations((prev) =>
            prev.map((conv) => (conv.id === event.payload.conversationId ? updatedConvo : conv)),
          );
        },
      );

      const unsubscribeMessageReceivedEvent = eventBus.subscribe<MessageReceivedEvent>(
        EventType.MESSAGE_RECEIVED,
        async (event) => {
          if (!session) return;
          const updatedConvo = await getConversationUseCase.execute(
            event.payload.conversationId,
            session.user,
          );
          if (!updatedConvo) return;
          setConversations((prev) =>
            prev.map((conv) => (conv.id === event.payload.conversationId ? updatedConvo : conv)),
          );
        },
      );

      const unsubscribeConversationAssignedEvent = eventBus.subscribe<ConversationAssignedEvent>(
        EventType.CONVERSATION_ASSIGNED,
        async (event) => {
          setConversations((prev) =>
            prev.map((conv) =>
              conv.id === event.payload.conversationId
                ? {
                    ...conv,
                    assignedToUserId: event.payload.userId,
                    assignedToUserName: event.payload.userName,
                  }
                : conv,
            ),
          );

          // Mark as read if assigned to current user
          if (session && event.payload.userId === session.user.id) {
            try {
              await markConversationAsReadUseCase.execute(event.payload.conversationId);
            } catch (error) {
              console.error("Failed to mark conversation as read after assignment:", error);
            }
          }
        },
      );

      const unsubscribeConversationReadEvent = eventBus.subscribe<ConversationReadEvent>(
        EventType.CONVERSATION_READ,
        async (event) => {
          // Update unread count locally - no need to fetch from API
          setConversations((prev) =>
            prev.map((conv) =>
              conv.id === event.payload.conversationId ? { ...conv, unread: 0 } : conv,
            ),
          );
        },
      );

      return () => {
        unsubscribeMessageSentEvent();
        unsubscribeMessageReceivedEvent();
        unsubscribeConversationAssignedEvent();
        unsubscribeConversationReadEvent();
      };
    }
  }, [session, loadConversations, eventBus]);

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

  return {
    conversations,
    setConversations,
    loading,
    error,
    reload: loadConversations,
    search,
  };
}

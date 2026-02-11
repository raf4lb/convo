import { useCallback, useEffect, useState } from "react";

import { useAuth } from "./useAuth";
import { useConversationMessages } from "./useConversationMessages";
import { useUsers } from "./useUsers";

import { Conversation } from "@/domain/entities/Conversation";
import { Permission } from "@/domain/entities/Permission";
import { UserRole } from "@/domain/entities/User";
import {
  ConversationAssignedEvent,
  ConversationAssignedPayload,
} from "@/domain/events/ConversationAssignedEvent";
import { EventType } from "@/domain/events/IDomainEvent";
import { IEventBus } from "@/domain/ports/IEventBus";
import {
  assignConversationToAttendantUseCase,
  getConversationUseCase,
} from "@/infrastructure/di/container";

export function useChatAreaState(conversationId: string | null, eventBus: IEventBus) {
  const { session, hasPermission } = useAuth();
  const { messages, loading, isSendingMessage, sendMessage } = useConversationMessages(
    conversationId,
    eventBus,
  );
  const { users } = useUsers();
  const [conversation, setConversation] = useState<Conversation | null>(null);
  const [openAssignPopover, setOpenAssignPopover] = useState(false);
  const [messageText, setMessageText] = useState("");

  const onConversationAssigned = useCallback((payload: ConversationAssignedPayload) => {
    setConversation((prev) => {
      if (!prev) return prev;
      return {
        ...prev,
        assignedToUserId: payload.userId,
        assignedToUserName: payload.userName,
      };
    });
  }, []);

  useEffect(() => {
    const loadConversation = async () => {
      const conversation =
        conversationId && session
          ? await getConversationUseCase.execute(conversationId, session.user)
          : null;
      setConversation(conversation);
    };
    loadConversation();

    const unsubscribeConversationAssignedEvent = eventBus.subscribe<ConversationAssignedEvent>(
      EventType.CONVERSATION_ASSIGNED,
      async (event) => {
        onConversationAssigned(event.payload);
      },
    );

    return () => {
      unsubscribeConversationAssignedEvent();
    };
  }, [conversationId, session, eventBus, onConversationAssigned]);

  const canAssingConversation = hasPermission(Permission.ASSIGN_CONVERSATION);

  const handleAssignAttendant = async (userId: string | null, userName: string | null) => {
    if (conversationId) {
      await assignConversationToAttendantUseCase.execute(conversationId, userId, userName);
      if (conversation)
        setConversation({
          ...conversation,
          assignedToUserId: userId,
          assignedToUserName: userName,
        });
      setOpenAssignPopover(false);
    }
  };

  const handleSendMessage = async () => {
    if (!messageText || !conversationId || !session) return;

    if (conversation?.assignedToUserId !== session.user.id) return;

    await sendMessage(messageText, session.user.name);
    setMessageText("");
  };

  const isSendMessageBlocked =
    isSendingMessage || conversation?.assignedToUserId !== session?.user.id;

  const assignConversationToUser = async () => {
    if (!session) return;
    handleAssignAttendant(session.user.id, session.user.name);
  };

  const canAssignConversationToUser =
    session &&
    conversation &&
    conversation.assignedToUserId !== session.user.id &&
    session.user.role === UserRole.ATTENDANT;

  return {
    session,
    hasPermission,
    messages,
    loading,
    isSendingMessage,
    sendMessage,
    users,
    openAssignPopover,
    setOpenAssignPopover,
    messageText,
    setMessageText,
    canAssingConversation,
    conversation,
    handleAssignAttendant,
    canAssignConversationToUser,
    assignConversationToUser,
    handleSendMessage,
    isSendMessageBlocked,
  };
}

import { useEffect } from "react";

import {
  ArrowLeft,
  Check,
  Headset,
  MoreVertical,
  Paperclip,
  Send,
  Smile,
  User,
} from "lucide-react";

import { Avatar, AvatarFallback } from "../../components/ui/avatar";
import { Badge } from "../../components/ui/badge";
import { Button } from "../../components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
} from "../../components/ui/command";
import { Input } from "../../components/ui/input";
import { Popover, PopoverContent, PopoverTrigger } from "../../components/ui/popover";
import { TabType } from "../constants/tabTypes";
import { useChatAreaState } from "../hooks/useChatAreaState";
import { useScrollToBottom } from "../hooks/useScrollToBottom";

import { eventBus } from "@/infrastructure/di/container.ts";

interface ChatAreaProps {
  conversationId: string | null;
  onBack?: () => void;
  activeTab?: TabType;
}

export function ChatArea({ conversationId, onBack, activeTab }: ChatAreaProps) {
  const chatAreaState = useChatAreaState(conversationId, eventBus, activeTab);
  const { scrollRef, scrollToBottom, isNearBottom } = useScrollToBottom();

  const conversation = chatAreaState.conversation;
  const users = chatAreaState.users;
  const messages = chatAreaState.messages;

  // Scroll to bottom when conversation changes
  useEffect(() => {
    if (!chatAreaState.loading && messages.length > 0 && conversationId) {
      // Use setTimeout to ensure DOM has rendered
      setTimeout(() => {
        scrollToBottom("auto");
      }, 0);
    }
  }, [conversationId, chatAreaState.loading, messages.length, scrollToBottom]);

  // Scroll to bottom when new messages arrive (if user is near bottom)
  useEffect(() => {
    if (!chatAreaState.loading && messages.length > 0 && isNearBottom) {
      // Use smooth scroll for new messages
      setTimeout(() => {
        scrollToBottom("smooth");
      }, 0);
    }
  }, [messages.length, isNearBottom, chatAreaState.loading, scrollToBottom]);

  const buildAssignButton = () => {
    if (chatAreaState.canAssingConversation) {
      return (
        <Popover
          open={chatAreaState.openAssignPopover}
          onOpenChange={chatAreaState.setOpenAssignPopover}
        >
          <PopoverTrigger asChild>
            <Button variant="ghost" size="sm" className="gap-2">
              <User className="w-4 h-4" />
              {"Atribuir"}
            </Button>
          </PopoverTrigger>
          <PopoverContent className="p-0" align="end">
            <Command>
              <CommandInput placeholder="Buscar atendente..." />
              <CommandEmpty>Nenhum atendente encontrado.</CommandEmpty>
              <CommandGroup>
                <CommandItem
                  onSelect={() => chatAreaState.handleAssignAttendant(null, null)}
                  className="cursor-pointer"
                >
                  <Check
                    className={`mr-2 h-4 w-4 ${
                      !conversation?.assignedToUserId ? "opacity-100" : "opacity-0"
                    }`}
                  />
                  Não atribuída
                </CommandItem>
                {users.map((attendant) => (
                  <CommandItem
                    key={attendant.id}
                    value={attendant.name}
                    onSelect={() =>
                      chatAreaState.handleAssignAttendant(attendant.id, attendant.name)
                    }
                    className="cursor-pointer"
                  >
                    <Check
                      className={`mr-2 h-4 w-4 ${
                        conversation?.assignedToUserId === attendant.id
                          ? "opacity-100"
                          : "opacity-0"
                      }`}
                    />
                    <div className="flex items-center gap-2">
                      <div className="w-6 h-6 rounded-full bg-linear-to-br from-green-400 to-green-600 flex items-center justify-center text-white text-xs">
                        {attendant.name
                          .split(" ")
                          .map((n) => n[0])
                          .join("")
                          .substring(0, 2)}
                      </div>
                      <div>
                        <p className="text-sm">
                          {attendant.name !== chatAreaState.session?.user.name
                            ? attendant.name
                            : attendant.name + " (Eu)"}
                        </p>
                        <p className="text-xs text-neutral-500">{attendant.email}</p>
                      </div>
                    </div>
                  </CommandItem>
                ))}
              </CommandGroup>
            </Command>
          </PopoverContent>
        </Popover>
      );
    } else if (chatAreaState.canAssignConversationToUser) {
      return (
        <Button
          variant="ghost"
          size="sm"
          className="gap-2"
          onClick={() => chatAreaState.assignConversationToUser()}
        >
          <Headset className="w-4 h-4" /> Atender
        </Button>
      );
    }
  };

  if (!conversationId) {
    return (
      <div className="flex-1 flex items-center justify-center bg-neutral-50">
        <div className="text-center text-neutral-400">
          <MessageSquare className="w-16 h-16 mx-auto mb-4" />
          <p>Selecione uma conversa para começar</p>
        </div>
      </div>
    );
  }

  if (chatAreaState.loading) {
    return (
      <div className="flex-1 flex items-center justify-center bg-white">
        <p className="text-neutral-500">Carregando mensagens...</p>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col bg-white">
      {/* Chat Header */}
      <div className="h-16 border-b border-neutral-200 px-6 flex items-center justify-between">
        <div className="flex items-center gap-3">
          {onBack && (
            <Button variant="ghost" size="icon" className="md:hidden" onClick={onBack}>
              <ArrowLeft className="w-5 h-5" />
            </Button>
          )}
          <Avatar>
            <AvatarFallback className="bg-linear-to-br from-green-400 to-green-600 text-white">
              {conversation?.customerName.charAt(0) || "U"}
            </AvatarFallback>
          </Avatar>
          <div>
            <h3 className="text-neutral-900">{conversation?.customerName || "Usuário"}</h3>
            <p className="text-xs text-neutral-500">{conversation?.customerPhone || ""}</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {!conversation?.assignedToUserId ? (
            <Badge
              variant="outline"
              className="text-xs border-amber-200 text-amber-700 bg-amber-50"
            >
              Não atribuída
            </Badge>
          ) : conversation.assignedToUserId != chatAreaState.session?.user.id ? (
            <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
              <span className="flex items-center gap-1">
                <Headset className="w-3 h-3" />
                {conversation.assignedToUserName}
              </span>
            </Badge>
          ) : (
            <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200">
              <span className="flex items-center gap-1">
                <Headset className="w-3 h-3" /> Você
              </span>
            </Badge>
          )}
          {buildAssignButton()}
          <Button variant="ghost" size="icon">
            <MoreVertical className="w-5 h-5" />
          </Button>
        </div>
      </div>

      {/* Messages */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === "customer" ? "justify-start" : "justify-end"}`}
          >
            <div
              className={`max-w-md px-4 py-2.5 rounded-2xl ${
                message.sender === "customer"
                  ? "bg-neutral-100 text-neutral-900"
                  : "bg-green-500 text-white"
              }`}
            >
              {message.sender === "attendant" && message.attendantName && (
                <p className="text-xs opacity-80 mb-1">
                  {message.attendantName !== chatAreaState.session?.user.name
                    ? message.attendantName
                    : "Você"}
                </p>
              )}
              <p className="text-sm">{message.text}</p>
              <p
                className={`text-xs mt-1 ${
                  message.sender === "customer" ? "text-neutral-500" : "text-green-100"
                }`}
              >
                {message.timestamp}
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* Input Area */}
      <div className="border-t border-neutral-200 p-4">
        <div className="flex items-center gap-2">
          <Button
            disabled={chatAreaState.isSendMessageBlocked}
            variant="ghost"
            size="icon"
            className="shrink-0"
          >
            <Paperclip className="w-5 h-5" />
          </Button>

          <Input
            placeholder="Digite sua mensagem..."
            className="flex-1 border-neutral-200"
            value={chatAreaState.messageText}
            onChange={(e) => chatAreaState.setMessageText(e.target.value)}
            disabled={chatAreaState.isSendMessageBlocked}
          />

          <Button
            disabled={chatAreaState.isSendMessageBlocked}
            variant="ghost"
            size="icon"
            className="shrink-0"
          >
            <Smile className="w-5 h-5" />
          </Button>

          <Button
            size="icon"
            className="shrink-0 bg-green-500 hover:bg-green-600"
            onClick={chatAreaState.handleSendMessage}
            disabled={chatAreaState.isSendMessageBlocked}
          >
            <Send className="w-5 h-5" />
          </Button>
        </div>
      </div>
    </div>
  );
}

function MessageSquare({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      fill="none"
      strokeWidth="1.5"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z"
      />
    </svg>
  );
}

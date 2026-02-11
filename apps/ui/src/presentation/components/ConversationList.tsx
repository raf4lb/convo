import { Headset } from "lucide-react";

import { Badge } from "../../components/ui/badge";
import { useAuth } from "../hooks/useAuth";

import { Conversation } from "@/domain/entities/Conversation.ts";
import { UserRole } from "@/domain/entities/User.ts";

interface ConversationListProps {
  selectedConversation: string | null;
  onSelectConversation: (id: string) => void;
  conversations: Conversation[];
}

export function ConversationList({
  selectedConversation,
  onSelectConversation,
  conversations,
}: ConversationListProps) {
  const { session } = useAuth();

  if (!session) throw new Error("No session");

  return (
    <div className="flex-1 overflow-y-auto">
      {conversations.length === 0 ? (
        <p className="text-neutral-500 text-center p-4">Nenhuma conversa encontrada</p>
      ) : (
        conversations.map((conversation) => {
          const isSelected = selectedConversation === conversation.id;

          return (
            <button
              key={conversation.id}
              onClick={() => onSelectConversation(conversation.id)}
              className={`w-full p-4 border-b border-neutral-100 hover:bg-neutral-50 transition-colors text-left ${
                isSelected ? "bg-green-50" : ""
              }`}
            >
              <div className="flex items-start gap-3">
                {/* Avatar */}
                <div className="w-11 h-11 rounded-full bg-linear-to-br from-green-400 to-green-600 flex items-center justify-center shrink-0 text-white">
                  {conversation.customerName
                    .split(" ")
                    .map((n) => n[0])
                    .join("")
                    .substring(0, 2)}
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between mb-1">
                    <div className="flex-1 min-w-0">
                      <h3 className="text-neutral-900 truncate">{conversation.customerName}</h3>
                      <p className="text-xs text-neutral-500">{conversation.customerPhone}</p>
                    </div>
                    <span className="text-xs text-neutral-500 ml-2 shrink-0">
                      {conversation.time}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <p
                      className="text-sm text-neutral-600 truncate mb-2 mt-2 mr-2"
                      title={conversation.lastMessage}
                    >
                      {conversation.lastMessage}
                    </p>
                    {conversation.unread > 0 && (
                      <Badge className="bg-green-500 text-white text-xs h-5 min-w-5 rounded-full flex items-center justify-center">
                        {conversation.unread}
                      </Badge>
                    )}
                  </div>

                  {!conversation.assignedToUserId ? (
                    <Badge
                      variant="outline"
                      className="text-xs border-amber-200 text-amber-700 bg-amber-50"
                    >
                      Não atribuída
                    </Badge>
                  ) : (
                    (session.company.attendantSeesAllConversations ||
                      session.user.role !== UserRole.ATTENDANT) &&
                    (conversation.assignedToUserId != session.user.id ? (
                      <Badge
                        variant="outline"
                        className="bg-green-50 text-green-700 border-green-200"
                      >
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
                    ))
                  )}
                </div>
              </div>
            </button>
          );
        })
      )}
    </div>
  );
}

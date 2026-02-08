import { useState } from "react";

import { Search, TestTubeDiagonal } from "lucide-react";

import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { ConversationStatus } from "../../domain/entities/Conversation";
import { eventBus, messagesWebSocket } from "../../infrastructure/di/container";
import { useAuth } from "../contexts/AuthContext";
import { useConversations } from "../hooks/useConversations";

import { ChatArea } from "./ChatArea";
import { ConversationList } from "./ConversationList";
import { ConversationLoading } from "./ConversationLoading";

export enum TabType {
  ALL = "all",
  PENDING = "pending",
  RESOLVED = "resolved",
  UNASSIGNED = "unassigned",
}

export function Chat() {
  const { session } = useAuth();
  const [searchQuery, setSearchQuery] = useState("");
  const [activeTab, setActiveTab] = useState<TabType>(TabType.UNASSIGNED);
  const conversationsHook = useConversations(eventBus);

  const [selectedConversationId, setSelectedConversationId] = useState<string | null>(null);

  if (!session) throw new Error("No session");

  const handleTabChange = async (tab: TabType) => {
    setActiveTab(tab);
    await handleSearch(searchQuery);
  };

  const handleSearch = async (query: string) => {
    setSearchQuery(query);
    if (query && query.trim()) {
      await conversationsHook.search(query);
    } else {
      await conversationsHook.reload();
    }
  };

  let filteredConversations = conversationsHook.conversations.filter((conv) => {
    if (activeTab === TabType.UNASSIGNED) return conv.assignedToUserId === null;
    if (activeTab === TabType.PENDING) return conv.unread > 0 && conv.assignedToUserId !== null;
    if (activeTab === TabType.RESOLVED) return conv.status === ConversationStatus.RESOLVED;
    return true; // 'all'
  });

  filteredConversations = [...filteredConversations].sort(
    (a, b) => b.updatedAt.getTime() - a.updatedAt.getTime(),
  );

  return (
    <>
      <div className="w-96 bg-white border-r border-neutral-200 flex flex-col">
        {/* Header */}
        <div className="p-4 border-b border-neutral-200">
          {/* <h2 className="mb-4">Conversas</h2> */}
          <div className="flex justify-between">
            <h2 className="mb-4">Conversas</h2>
            <Button
              className="flex-col mb-4"
              onClick={() => {
                console.log("sending test message");
                const message = {
                  conversationId: "948ed322-a961-46fd-b533-363103e94d3a",
                  text: "Olá",
                  timestamp: new Date(),
                  sender: "customer",
                  attendantName: "João Silva",
                  id: Math.random().toString(),
                };
                messagesWebSocket.send(JSON.stringify(message));
              }}
            >
              <TestTubeDiagonal />
            </Button>
          </div>

          {/* Search */}
          <div className="relative mb-3">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-neutral-400" />
            <Input
              placeholder="Buscar conversas..."
              className="pl-9 bg-neutral-50 border-0"
              onChange={async (e) => {
                await handleSearch(e.target.value);
              }}
            />
          </div>

          {/* Filter Tabs */}
          <div className="flex gap-1 overflow-x-auto">
            <button
              onClick={() => handleTabChange(TabType.UNASSIGNED)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap ${
                activeTab === TabType.UNASSIGNED
                  ? "border-amber-200 text-amber-700 bg-amber-50"
                  : "text-amber-600 bg-neutral-100 hover:bg-neutral-50"
              }`}
            >
              Não atribuídas
            </button>
            <button
              onClick={() => handleTabChange(TabType.PENDING)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap ${
                activeTab === TabType.PENDING
                  ? "bg-green-50 text-green-600"
                  : "text-neutral-600 bg-neutral-100 hover:bg-neutral-50"
              }`}
            >
              Pendentes
            </button>
            <button
              onClick={() => handleTabChange(TabType.ALL)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap ${
                activeTab === TabType.ALL
                  ? "bg-green-50 text-green-600"
                  : "text-neutral-600 bg-neutral-100 hover:bg-neutral-50"
              }`}
            >
              Todas
            </button>
            <button
              onClick={() => handleTabChange(TabType.RESOLVED)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap ${
                activeTab === TabType.RESOLVED
                  ? "bg-green-50 text-green-600"
                  : "text-neutral-600 bg-neutral-100 hover:bg-neutral-50"
              }`}
            >
              Resolvidas
            </button>
          </div>
        </div>

        {/* Conversation List */}
        {conversationsHook.loading ? (
          <ConversationLoading />
        ) : (
          <ConversationList
            selectedConversation={selectedConversationId}
            onSelectConversation={setSelectedConversationId}
            conversations={filteredConversations}
          />
        )}
      </div>

      {/* Chat Area */}
      <ChatArea conversationId={selectedConversationId} />
    </>
  );
}

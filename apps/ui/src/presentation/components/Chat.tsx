import { useEffect, useRef, useState } from "react";

import { Search, TestTubeDiagonal } from "lucide-react";

import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { TabType } from "../constants/tabTypes";
import { useAuth } from "../hooks/useAuth";
import { useConversations } from "../hooks/useConversations";

import { ChatArea } from "./ChatArea";
import { ConversationList } from "./ConversationList";
import { ConversationLoading } from "./ConversationLoading";

import { useIsMobile } from "@/components/ui/use-mobile.ts";
import { eventBus, messagesWebSocket } from "@/infrastructure/di/container.ts";

const MIN_WIDTH = 280;
const MAX_WIDTH = 600;
const DEFAULT_WIDTH = 384;

export function Chat() {
  const { session } = useAuth();
  const [searchQuery, setSearchQuery] = useState("");
  const [activeTab, setActiveTab] = useState<TabType>(TabType.UNASSIGNED);
  const conversationsHook = useConversations(eventBus, activeTab);

  const [selectedConversationId, setSelectedConversationId] = useState<string | null>(null);
  const isMobile = useIsMobile();
  const [conversationListWidth, setConversationListWidth] = useState(DEFAULT_WIDTH);
  const [isResizing, setIsResizing] = useState(false);
  const [startX, setStartX] = useState(0);
  const [startWidth, setStartWidth] = useState(DEFAULT_WIDTH);

  if (!session) throw new Error("No session");

  const searchTimeoutRef = useRef<NodeJS.Timeout>();

  const handleTabChange = (tab: TabType) => {
    // Cancel any pending search
    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }
    setActiveTab(tab);
    setSearchQuery(""); // Clear search when changing tabs
  };

  const handleSearchInput = (query: string) => {
    setSearchQuery(query);

    // Clear existing timeout
    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }

    // Debounce search by 300ms
    searchTimeoutRef.current = setTimeout(() => {
      if (query && query.trim()) {
        conversationsHook.search(query);
      } else {
        conversationsHook.reload();
      }
    }, 300);
  };

  // Cleanup timeout on unmount
  useEffect(() => {
    return () => {
      if (searchTimeoutRef.current) {
        clearTimeout(searchTimeoutRef.current);
      }
    };
  }, []);

  // Sort conversations by updated date
  const sortedConversations = [...conversationsHook.conversations].sort(
    (a, b) => b.updatedAt.getTime() - a.updatedAt.getTime(),
  );

  const handleMouseDown = (e: React.MouseEvent) => {
    e.preventDefault();
    setIsResizing(true);
    setStartX(e.clientX);
    setStartWidth(conversationListWidth);
  };

  const handleMouseMove = (e: MouseEvent) => {
    if (!isResizing) return;
    const delta = e.clientX - startX;
    const newWidth = startWidth + delta;
    if (newWidth >= MIN_WIDTH && newWidth <= MAX_WIDTH) {
      setConversationListWidth(newWidth);
    }
  };

  const handleMouseUp = () => {
    setIsResizing(false);
  };

  // Add/remove mousemove and mouseup listeners
  useEffect(() => {
    if (isResizing) {
      window.addEventListener("mousemove", handleMouseMove);
      window.addEventListener("mouseup", handleMouseUp);
    }
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isResizing]);

  const conversationListContent = (
    <>
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
            value={searchQuery}
            onChange={(e) => {
              handleSearchInput(e.target.value);
            }}
          />
        </div>

        {/* Filter Tabs */}
        <div className="flex gap-1 overflow-x-auto">
          <button
            onClick={() => handleTabChange(TabType.UNASSIGNED)}
            className={`flex-1 px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap ${
              activeTab === TabType.UNASSIGNED
                ? "border-amber-200 text-amber-700 bg-amber-50"
                : "text-amber-600 bg-neutral-100 hover:bg-neutral-50"
            }`}
          >
            Não atribuídas
          </button>
          <button
            onClick={() => handleTabChange(TabType.PENDING)}
            className={`flex-1 px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap ${
              activeTab === TabType.PENDING
                ? "bg-green-50 text-green-600"
                : "text-neutral-600 bg-neutral-100 hover:bg-neutral-50"
            }`}
          >
            Pendentes
          </button>
          <button
            onClick={() => handleTabChange(TabType.ALL)}
            className={`flex-1 px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap ${
              activeTab === TabType.ALL
                ? "bg-green-50 text-green-600"
                : "text-neutral-600 bg-neutral-100 hover:bg-neutral-50"
            }`}
          >
            Todas
          </button>
          <button
            onClick={() => handleTabChange(TabType.RESOLVED)}
            className={`flex-1 px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap ${
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
          conversations={sortedConversations}
        />
      )}
    </>
  );

  return (
    <>
      {isMobile ? (
        // Mobile: Single panel view
        selectedConversationId ? (
          // Show ChatArea when conversation selected
          <ChatArea
            conversationId={selectedConversationId}
            onBack={() => setSelectedConversationId(null)}
            activeTab={activeTab}
          />
        ) : (
          // Show ConversationList when no selection
          <div className="flex-1 bg-white flex flex-col">{conversationListContent}</div>
        )
      ) : (
        // Desktop: Two-panel layout
        <>
          <div
            className="bg-white border-r border-neutral-200 flex flex-col relative"
            style={{ width: `${conversationListWidth}px` }}
          >
            {conversationListContent}
            {/* Resize Handle */}
            <button
              type="button"
              aria-label="Resize conversation list"
              className="absolute top-0 right-0 w-1 h-full cursor-col-resize hover:bg-green-500 transition-colors bg-transparent border-0 p-0"
              onMouseDown={handleMouseDown}
              onKeyDown={(e) => {
                if (e.key === "ArrowLeft") {
                  setConversationListWidth((prev) => Math.max(MIN_WIDTH, prev - 20));
                } else if (e.key === "ArrowRight") {
                  setConversationListWidth((prev) => Math.min(MAX_WIDTH, prev + 20));
                }
              }}
            />
          </div>
          <ChatArea conversationId={selectedConversationId} activeTab={activeTab} />
        </>
      )}
    </>
  );
}

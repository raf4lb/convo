import { Conversation, ConversationStatus } from "../../domain/entities/Conversation";
import { Message } from "../../domain/entities/Message";
import { AuthUser } from "../../domain/entities/User";
import { IConversationRepository } from "../../domain/repositories/IConversationRepository";

const mockConversations: Conversation[] = [
  {
    id: "f4bf4e4e-935a-4fae-a6a5-e65292decc74",
    companyId: "474d2fd7-2e99-452b-a4db-fe93ecf8729c",
    customerId: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc085",
    customerName: "Maria Silva",
    customerPhone: "+55 11 98765-4321",
    lastMessage: "Gostaria de saber mais sobre os produtos",
    time: "10:30",
    unread: 2,
    assignedToUserId: "e8bf801b-d16a-4736-8df9-df9d9278293c",
    assignedToUserName: "João Silva",
    status: ConversationStatus.PENDING,
    createdAt: new Date("2024-11-12T10:00:00"),
    updatedAt: new Date("2024-11-12T10:30:00"),
  },
  {
    id: "2ef42cf2-24d6-4553-bb79-614558549602",
    companyId: "474d2fd7-2e99-452b-a4db-fe93ecf8729c",
    customerId: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc086",
    customerName: "Carlos Santos",
    customerPhone: "+55 21 99876-5432",
    lastMessage: "Obrigado pelo atendimento!",
    time: "09:15",
    unread: 0,
    assignedToUserId: "3b757f19-4cba-448a-b114-31d54c53adf9",
    assignedToUserName: "Ana Costa",
    status: ConversationStatus.ACTIVE,
    createdAt: new Date("2024-11-12T09:00:00"),
    updatedAt: new Date("2024-11-12T09:15:00"),
  },
  {
    id: "4e018edb-8219-445a-9bc1-9c8ddbf76da7",
    companyId: "474d2fd7-2e99-452b-a4db-fe93ecf8729c",
    customerId: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc087",
    customerName: "Fernanda Lima",
    customerPhone: "+55 11 91234-5678",
    lastMessage: "Quando vocês abrem?",
    time: "Ontem",
    unread: 1,
    assignedToUserId: null,
    assignedToUserName: null,
    status: ConversationStatus.PENDING,
    createdAt: new Date("2024-11-11T14:00:00"),
    updatedAt: new Date("2024-11-11T14:20:00"),
  },
  {
    id: "dbfd6c8a-41e3-4e95-b575-921983cea167",
    companyId: "474d2fd7-2e99-452b-a4db-fe93ecf8729c",
    customerId: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc088",
    customerName: "Pedro Oliveira",
    customerPhone: "+55 11 98888-7777",
    lastMessage: "Perfeito, vou aguardar",
    time: "Ontem",
    unread: 0,
    assignedToUserId: "e8bf801b-d16a-4736-8df9-df9d9278293c",
    assignedToUserName: "João Silva",
    status: ConversationStatus.RESOLVED,
    createdAt: new Date("2024-11-11T16:00:00"),
    updatedAt: new Date("2024-11-11T16:45:00"),
  },
  {
    id: "948ed322-a961-46fd-b533-363103e94d3a",
    companyId: "474d2fd7-2e99-452b-a4db-fe93ecf8729c",
    customerId: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc089",
    customerName: "Julia Costa",
    customerPhone: "+55 21 97777-6666",
    lastMessage: "Preciso de ajuda urgente",
    time: "11:45",
    unread: 3,
    assignedToUserId: null,
    assignedToUserName: null,
    status: ConversationStatus.PENDING,
    createdAt: new Date("2024-11-12T11:30:00"),
    updatedAt: new Date("2024-11-12T11:45:00"),
  },
];

const mockMessages: Record<string, Message[]> = {
  "f4bf4e4e-935a-4fae-a6a5-e65292decc74": [
    {
      id: "c20d1bfb-b570-4014-8756-4737a50ca76d",
      text: "Olá! Gostaria de saber mais sobre os produtos",
      timestamp: "10:28",
      sender: "customer",
    },
    {
      id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc062",
      text: "Olá Maria! Claro, ficarei feliz em ajudar. Temos diversas opções disponíveis.",
      timestamp: "10:29",
      sender: "attendant",
      attendantName: "João Silva",
    },
    {
      id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc063",
      text: "Vocês fazem entrega?",
      timestamp: "10:29",
      sender: "customer",
    },
    {
      id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc064",
      text: "Sim! Fazemos entregas para toda a cidade. O prazo varia de 2 a 5 dias úteis.",
      timestamp: "10:30",
      sender: "attendant",
      attendantName: "João Silva",
    },
    {
      id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc065",
      text: "Gostaria de saber mais sobre os produtos",
      timestamp: "10:30",
      sender: "customer",
    },
  ],
  "2ef42cf2-24d6-4553-bb79-614558549602": [
    {
      id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc066",
      text: "Bom dia! Gostaria de fazer uma reclamação sobre o produto",
      timestamp: "09:00",
      sender: "customer",
    },
    {
      id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc067",
      text: "Bom dia, Carlos! Sinto muito pelo inconveniente. Pode me contar o que aconteceu?",
      timestamp: "09:05",
      sender: "attendant",
      attendantName: "Ana Costa",
    },
    {
      id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc068",
      text: "O produto chegou com defeito",
      timestamp: "09:07",
      sender: "customer",
    },
    {
      id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc069",
      text: "Entendo. Vou providenciar a troca imediatamente. Pode me enviar uma foto?",
      timestamp: "09:10",
      sender: "attendant",
      attendantName: "Ana Costa",
    },
    {
      id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc070",
      text: "Claro, vou enviar agora",
      timestamp: "09:12",
      sender: "customer",
    },
    {
      id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc071",
      text: "Perfeito! Já estou abrindo o chamado de troca. Você receberá o produto novo em até 3 dias úteis.",
      timestamp: "09:14",
      sender: "attendant",
      attendantName: "Ana Costa",
    },
    {
      id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc072",
      text: "Obrigado pelo atendimento!",
      timestamp: "09:15",
      sender: "customer",
    },
  ],
  "4e018edb-8219-445a-9bc1-9c8ddbf76da7": [
    {
      id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc073",
      text: "Olá!",
      timestamp: "14:18",
      sender: "customer",
    },
    {
      id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc074",
      text: "Quando vocês abrem?",
      timestamp: "14:20",
      sender: "customer",
    },
  ],
  "dbfd6c8a-41e3-4e95-b575-921983cea167": [
    {
      id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc075",
      text: "Boa tarde! Vocês têm o produto X em estoque?",
      timestamp: "16:30",
      sender: "customer",
    },
    {
      id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc076",
      text: "Boa tarde, Pedro! Sim, temos disponível. Quantas unidades você precisa?",
      timestamp: "16:35",
      sender: "attendant",
      attendantName: "João Silva",
    },
    {
      id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc077",
      text: "Preciso de 5 unidades",
      timestamp: "16:37",
      sender: "customer",
    },
    {
      id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc078",
      text: "Temos sim! Vou separar para você. Pode retirar hoje ainda?",
      timestamp: "16:40",
      sender: "attendant",
      attendantName: "João Silva",
    },
    {
      id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc079",
      text: "Perfeito, vou aguardar",
      timestamp: "16:45",
      sender: "customer",
    },
  ],
  "948ed322-a961-46fd-b533-363103e94d3a": [
    {
      id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc080",
      text: "Socorro!",
      timestamp: "11:40",
      sender: "customer",
    },
    {
      id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc081",
      text: "Preciso de ajuda urgente",
      timestamp: "11:42",
      sender: "customer",
    },
    {
      id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc082",
      text: "Meu pedido não chegou e preciso dele hoje",
      timestamp: "11:45",
      sender: "customer",
    },
  ],
};

export class ConversationRepository implements IConversationRepository {
  private conversations: Conversation[] = [...mockConversations];
  private messages: Record<string, Message[]> = { ...mockMessages };

  async getAll(companyId: string): Promise<Conversation[]> {
    const conversations = this.conversations.filter((c) => c.companyId === companyId);
    return Promise.resolve([...conversations]);
  }

  async getById(companyId: string, id: string): Promise<Conversation | null> {
    const conversation = this.conversations.find((c) => c.id === id && c.companyId == companyId);
    return Promise.resolve(conversation || null);
  }

  async getByAttendant(user: AuthUser): Promise<Conversation[]> {
    const conversations = this.conversations.filter(
      (c) =>
        c.companyId === user.companyId &&
        (c.assignedToUserId == user.id || c.assignedToUserId == null),
    );
    return Promise.resolve([...conversations]);
  }

  async getMessages(conversationId: string): Promise<Message[]> {
    const messages = this.messages[conversationId] || [];
    return Promise.resolve([...messages]);
  }

  async assignAttendant(
    conversationId: string,
    userId: string | null,
    userName: string | null,
  ): Promise<void> {
    const conversation = this.conversations.find((c) => c.id === conversationId);
    if (conversation) {
      conversation.assignedToUserId = userId;
      conversation.assignedToUserName = userName;
      conversation.updatedAt = new Date();
    }
    return Promise.resolve();
  }

  async sendMessage(conversationId: string, message: Omit<Message, "id">): Promise<Message> {
    const newMessage: Message = {
      ...message,
      id: Date.now().toString(),
    };

    if (!this.messages[conversationId]) {
      this.messages[conversationId] = [];
    }

    this.messages[conversationId].push(newMessage);

    // Update conversation
    const conversation = this.conversations.find((c) => c.id === conversationId);
    if (conversation) {
      conversation.unread = 0;
      conversation.lastMessage = message.text;
      conversation.updatedAt = new Date();
    }

    return Promise.resolve(newMessage);
  }

  async receiveMessage(conversationId: string, message: Message): Promise<Message> {
    if (!this.messages[conversationId]) {
      this.messages[conversationId] = [];
    }

    this.messages[conversationId].push(message);

    // Update conversation
    const conversation = this.conversations.find((c) => c.id === conversationId);
    if (conversation) {
      conversation.lastMessage = message.text;
      conversation.unread++;
      conversation.updatedAt = new Date();
    }
    return Promise.resolve(message);
  }

  async search(companyId: string, query: string): Promise<Conversation[]> {
    const lowerQuery = query.toLowerCase();
    const conversations = this.conversations.filter(
      (c) =>
        c.companyId === companyId &&
        (c.customerName.toLowerCase().includes(lowerQuery) ||
          c.customerPhone.includes(query) ||
          c.lastMessage.toLowerCase().includes(lowerQuery)),
    );
    return Promise.resolve(conversations);
  }

  async getUnassigned(companyId: string): Promise<Conversation[]> {
    const conversations = this.conversations.filter(
      (c) => c.companyId === companyId && c.assignedToUserId === null,
    );
    return Promise.resolve(conversations);
  }
}

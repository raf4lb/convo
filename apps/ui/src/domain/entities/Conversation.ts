export enum ConversationStatus {
  ACTIVE = "active",
  PENDING = "pending",
  RESOLVED = "resolved",
}

export interface Conversation {
  id: string;
  companyId: string;
  customerId: string;
  customerName: string;
  customerPhone: string;
  lastMessage: string;
  time: string;
  unread: number;
  assignedToUserId: string | null;
  assignedToUserName: string | null;
  status: ConversationStatus;
  createdAt: Date;
  updatedAt: Date;
}

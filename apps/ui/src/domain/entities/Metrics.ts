export interface DashboardMetrics {
  totalConversations: number;
  averageResponseTime: string;
  satisfactionRate: number;
  activeAttendants: number;
  totalAttendants: number;
  activeConversationsCount: number;
  trend: {
    conversations: number;
    responseTime: number;
    satisfaction: number;
  };
}

export interface ConversationByDay {
  date: string;
  conversas: number;
  resolvidas: number;
}

export interface AttendantPerformance {
  name: string;
  conversas: number;
  satisfacao: number;
}

export interface HourlyData {
  hora: string;
  mensagens: number;
}

export interface StatusData {
  name: string;
  value: number;
  color: string;
}

export interface AttendantDetailedPerformance {
  name: string;
  total: number;
  active: number;
  resolved: number;
  avgTime: string;
  satisfaction: number;
}

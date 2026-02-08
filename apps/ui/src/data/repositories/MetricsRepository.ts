import {
  AttendantDetailedPerformance,
  AttendantPerformance,
  ConversationByDay,
  DashboardMetrics,
  HourlyData,
  StatusData,
} from "../../domain/entities/Metrics";
import { IMetricsRepository } from "../../domain/repositories/IMetricsRepository";

export class MetricsRepository implements IMetricsRepository {
  async getDashboardMetrics(): Promise<DashboardMetrics> {
    return Promise.resolve({
      totalConversations: 366,
      averageResponseTime: "2m 34s",
      satisfactionRate: 4.8,
      activeAttendants: 3,
      totalAttendants: 4,
      activeConversationsCount: 6,
      trend: {
        conversations: 12,
        responseTime: 18,
        satisfaction: 0.3,
      },
    });
  }

  async getConversationsByDay(): Promise<ConversationByDay[]> {
    return Promise.resolve([
      { date: "05/11", conversas: 45, resolvidas: 42 },
      { date: "06/11", conversas: 52, resolvidas: 48 },
      { date: "07/11", conversas: 38, resolvidas: 36 },
      { date: "08/11", conversas: 61, resolvidas: 58 },
      { date: "09/11", conversas: 55, resolvidas: 51 },
      { date: "10/11", conversas: 48, resolvidas: 45 },
      { date: "11/11", conversas: 67, resolvidas: 62 },
    ]);
  }

  async getAttendantPerformance(): Promise<AttendantPerformance[]> {
    return Promise.resolve([
      { name: "João", conversas: 45, satisfacao: 4.8 },
      { name: "Ana", conversas: 38, satisfacao: 4.9 },
      { name: "Carlos", conversas: 52, satisfacao: 4.6 },
      { name: "Mariana", conversas: 29, satisfacao: 4.7 },
    ]);
  }

  async getHourlyData(): Promise<HourlyData[]> {
    return Promise.resolve([
      { hora: "00h", mensagens: 2 },
      { hora: "03h", mensagens: 1 },
      { hora: "06h", mensagens: 5 },
      { hora: "09h", mensagens: 45 },
      { hora: "12h", mensagens: 38 },
      { hora: "15h", mensagens: 52 },
      { hora: "18h", mensagens: 41 },
      { hora: "21h", mensagens: 18 },
    ]);
  }

  async getStatusData(): Promise<StatusData[]> {
    return Promise.resolve([
      { name: "Resolvidas", value: 245, color: "#00a63e" },
      { name: "Em andamento", value: 18, color: "#3b82f6" },
      { name: "Pendentes", value: 12, color: "#f59e0b" },
    ]);
  }

  async getDetailedPerformance(): Promise<AttendantDetailedPerformance[]> {
    return Promise.resolve([
      {
        name: "João Silva",
        total: 45,
        active: 3,
        resolved: 42,
        avgTime: "2m 15s",
        satisfaction: 4.8,
      },
      {
        name: "Ana Costa",
        total: 38,
        active: 2,
        resolved: 36,
        avgTime: "2m 45s",
        satisfaction: 4.9,
      },
      {
        name: "Carlos Mendes",
        total: 52,
        active: 1,
        resolved: 51,
        avgTime: "2m 30s",
        satisfaction: 4.6,
      },
      {
        name: "Mariana Santos",
        total: 29,
        active: 0,
        resolved: 29,
        avgTime: "3m 10s",
        satisfaction: 4.7,
      },
    ]);
  }
}

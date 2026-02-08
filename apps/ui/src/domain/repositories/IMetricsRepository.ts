import {
  DashboardMetrics,
  ConversationByDay,
  AttendantPerformance,
  HourlyData,
  StatusData,
  AttendantDetailedPerformance,
} from "../entities/Metrics";

export interface IMetricsRepository {
  getDashboardMetrics(): Promise<DashboardMetrics>;
  getConversationsByDay(): Promise<ConversationByDay[]>;
  getAttendantPerformance(): Promise<AttendantPerformance[]>;
  getHourlyData(): Promise<HourlyData[]>;
  getStatusData(): Promise<StatusData[]>;
  getDetailedPerformance(): Promise<AttendantDetailedPerformance[]>;
}

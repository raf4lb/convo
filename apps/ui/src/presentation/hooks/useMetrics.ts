import { useState, useEffect } from "react";

import {
  DashboardMetrics,
  ConversationByDay,
  AttendantPerformance,
  HourlyData,
  StatusData,
  AttendantDetailedPerformance,
} from "@/domain/entities/Metrics.ts";
import { getDashboardMetricsUseCase, metricsRepository } from "@/infrastructure/di/container.ts";

export function useMetrics() {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [conversationsByDay, setConversationsByDay] = useState<ConversationByDay[]>([]);
  const [attendantPerformance, setAttendantPerformance] = useState<AttendantPerformance[]>([]);
  const [hourlyData, setHourlyData] = useState<HourlyData[]>([]);
  const [statusData, setStatusData] = useState<StatusData[]>([]);
  const [detailedPerformance, setDetailedPerformance] = useState<AttendantDetailedPerformance[]>(
    [],
  );
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    loadMetrics();
  }, []);

  const loadMetrics = async () => {
    try {
      setLoading(true);

      const [
        metricsData,
        conversationsData,
        performanceData,
        hourlyDataResult,
        statusDataResult,
        detailedPerformanceData,
      ] = await Promise.all([
        getDashboardMetricsUseCase.execute(),
        metricsRepository.getConversationsByDay(),
        metricsRepository.getAttendantPerformance(),
        metricsRepository.getHourlyData(),
        metricsRepository.getStatusData(),
        metricsRepository.getDetailedPerformance(),
      ]);

      setMetrics(metricsData);
      setConversationsByDay(conversationsData);
      setAttendantPerformance(performanceData);
      setHourlyData(hourlyDataResult);
      setStatusData(statusDataResult);
      setDetailedPerformance(detailedPerformanceData);
      setError(null);
    } catch (err) {
      setError(err as Error);
    } finally {
      setLoading(false);
    }
  };

  return {
    metrics,
    conversationsByDay,
    attendantPerformance,
    hourlyData,
    statusData,
    detailedPerformance,
    loading,
    error,
    reload: loadMetrics,
  };
}

import { DashboardMetrics } from "../entities/Metrics";
import { IMetricsRepository } from "../repositories/IMetricsRepository";

export class GetDashboardMetrics {
  constructor(private metricsRepository: IMetricsRepository) {}

  async execute(): Promise<DashboardMetrics> {
    return await this.metricsRepository.getDashboardMetrics();
  }
}

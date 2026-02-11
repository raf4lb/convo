import { AttendantStats } from "@/domain/entities/AttendantStats";
import { IAttendantStatsRepository } from "@/domain/repositories/IAttendantStatsRepository";

const mockStats: AttendantStats[] = [
  {
    userId: "e8bf801b-d16a-4736-8df9-df9d9278293c",
    companyId: "474d2fd7-2e99-452b-a4db-fe93ecf8729c",
    status: "online",
    activeChats: 3,
    totalChats: 45,
    lastStatusChange: new Date(),
  },
  {
    userId: "3b757f19-4cba-448a-b114-31d54c53adf9",
    companyId: "474d2fd7-2e99-452b-a4db-fe93ecf8729c",
    status: "online",
    activeChats: 2,
    totalChats: 38,
    lastStatusChange: new Date(),
  },
  {
    userId: "23d04704-3770-4e4e-b5fe-b73359a400f5",
    companyId: "474d2fd7-2e99-452b-a4db-fe93ecf8729c",
    status: "away",
    activeChats: 1,
    totalChats: 52,
    lastStatusChange: new Date(),
  },
];

export class AttendantStatsRepository implements IAttendantStatsRepository {
  private stats: AttendantStats[] = [...mockStats];

  async getByUserId(userId: string): Promise<AttendantStats | null> {
    const stat = this.stats.find((s) => s.userId === userId);
    return Promise.resolve(stat || null);
  }

  async getByCompanyId(companyId: string): Promise<AttendantStats[]> {
    const stats = this.stats.filter((s) => s.companyId === companyId);
    return Promise.resolve(stats);
  }

  async updateStatus(userId: string, status: "online" | "away" | "offline"): Promise<void> {
    const stat = this.stats.find((s) => s.userId === userId);
    if (stat) {
      stat.status = status;
      stat.lastStatusChange = new Date();
    }
    return Promise.resolve();
  }

  async updateChatCounts(userId: string, activeChats: number, totalChats: number): Promise<void> {
    const stat = this.stats.find((s) => s.userId === userId);
    if (stat) {
      stat.activeChats = activeChats;
      stat.totalChats = totalChats;
    }
    return Promise.resolve();
  }
}

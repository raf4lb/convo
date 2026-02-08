import { AttendantStats } from "../entities/AttendantStats";

export interface IAttendantStatsRepository {
  getByUserId(userId: string): Promise<AttendantStats | null>;
  getByCompanyId(companyId: string): Promise<AttendantStats[]>;
  updateStatus(userId: string, status: "online" | "away" | "offline"): Promise<void>;
  updateChatCounts(userId: string, activeChats: number, totalChats: number): Promise<void>;
}

export interface AttendantStats {
  userId: string;
  companyId: string;
  status: "online" | "away" | "offline";
  activeChats: number;
  totalChats: number;
  lastStatusChange: Date;
}

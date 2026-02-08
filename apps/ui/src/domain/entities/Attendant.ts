export interface Attendant {
  id: string;
  name: string;
  email: string;
  status: "online" | "away" | "offline";
  activeChats: number;
  totalChats: number;
}

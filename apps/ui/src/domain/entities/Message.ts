export interface Message {
  id: string;
  text: string;
  timestamp: string;
  sender: "customer" | "attendant";
  attendantName?: string;
}

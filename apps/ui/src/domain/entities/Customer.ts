export interface Customer {
  id: string;
  companyId: string;
  name: string;
  phone: string;
  email: string | null;
  tags: string[];
  notes: string | null;
  createdAt: Date;
  lastContactAt: Date | null;
  isBlocked: boolean;
}

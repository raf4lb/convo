import { Company } from "../entities/Company";

export interface ICompanyRepository {
  getById(id: string): Promise<Company | null>;
  getAll(): Promise<Company[]>;
  create(company: Omit<Company, "id" | "createdAt">): Promise<Company>;
  update(
    id: string,
    name: string,
    email: string,
    phone: string,
    whatsappApiKey: string | null,
    attendantSeesAllConversations: boolean,
  ): Promise<Company>;
  delete(id: string): Promise<void>;
}

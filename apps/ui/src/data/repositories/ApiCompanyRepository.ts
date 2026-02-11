import { CompanyDTO, mapToCompany } from "./ApiMappers";

import { Company } from "@/domain/entities/Company";
import { ICompanyRepository } from "@/domain/repositories/ICompanyRepository";
import { HttpClient } from "@/infrastructure/http/HttpClient";


export class ApiCompanyRepository implements ICompanyRepository {
  constructor(private readonly client: HttpClient) {}

  async getById(id: string): Promise<Company | null> {
    const path = `/companies/${id}`;
    const res = await this.client.get(path);
    const body = res.data;
    return body ? mapToCompany(body as CompanyDTO) : null;
  }

  async getAll(): Promise<Company[]> {
    const path = "/companies/";
    const res = await this.client.get(path);
    const body = res.data;
    if (!Array.isArray(body)) {
      throw new Error("Invalid API response");
    }
    return body.map((d: CompanyDTO) => mapToCompany(d));
  }

  async create(data: Omit<Company, "id" | "createdAt">): Promise<Company> {
    // const company: Company = {
    //   ...data,
    //   id: Date.now().toString(),
    //   createdAt: new Date(),
    // };
    throw new Error("Not implemented");
  }

  async update(
    id: string,
    name: string,
    email: string,
    phone: string,
    whatsappApiKey: string | null,
    attendantSeesAllConversations: boolean,
  ): Promise<Company> {
    const path = `/companies/${id}`;
    const payload = {
      name,
      email,
      phone,
      whatsapp_api_key: whatsappApiKey,
      attendant_sees_all_conversations: attendantSeesAllConversations,
    };
    const res = await this.client.patch(path, { body: payload });
    const body = res.data;
    return mapToCompany(body as CompanyDTO);
  }

  async delete(id: string): Promise<void> {
    throw new Error("Not implemented");
  }
}

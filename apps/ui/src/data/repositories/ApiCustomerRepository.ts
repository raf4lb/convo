import { CustomerDTO, mapToCustomer } from "./ApiMappers";

import { Customer } from "@/domain/entities/Customer";
import { ICustomerRepository } from "@/domain/repositories/ICustomerRepository";
import { HttpClient } from "@/infrastructure/http/HttpClient";


export class ApiCustomerRepository implements ICustomerRepository {
  constructor(private readonly client: HttpClient) {}

  async getById(id: string): Promise<Customer | null> {
    const path = `/contacts/${id}`;
    const res = await this.client.get(path);
    const body = res.data;
    return body ? mapToCustomer(body as CustomerDTO) : null;
  }

  async getByCompanyId(companyId: string): Promise<Customer[]> {
    const path = `/contacts/company/${companyId}`;
    const res = await this.client.get(path);
    const body = res.data.results;
    if (!Array.isArray(body)) {
      throw new Error("Invalid API response");
    }

    return body.map((customer: CustomerDTO) => mapToCustomer(customer));
  }

  async getByPhone(phone: string, companyId: string): Promise<Customer | null> {
    const path = `/contacts/company/${companyId}/phone/${phone}`;
    const res = await this.client.get(path);
    if (res.status === 404) return null;
    const body = res.data;
    return body ? mapToCustomer(body as CustomerDTO) : null;
  }

  async search(companyId: string, query: string): Promise<Customer[]> {
    const path = "/contacts/search";
    const res = await this.client.get(path, { query: { company_id: companyId, query: query } });
    const body = res.data.results;
    if (!Array.isArray(body)) {
      throw new Error("Invalid API response");
    }

    return body.map((customer: CustomerDTO) => mapToCustomer(customer));
  }

  async create(
    companyId: string,
    name: string,
    phone: string,
    email: string | null,
    tags: string[],
    notes: string | null,
  ): Promise<Customer> {
    const path = "/contacts/";
    const payload = {
      name,
      email,
      tags,
      notes,
      phone_number: phone,
      company_id: companyId,
    };
    const res = await this.client.post(path, { body: payload });
    const body = res.data;
    return mapToCustomer(body as CustomerDTO);
  }

  async update(id: string, updates: Partial<Customer>): Promise<Customer> {
    // const index = this.customers.findIndex((c) => c.id === id);
    // if (index === -1) {
    //   throw new Error("Customer not found");
    // }
    // this.customers[index] = { ...this.customers[index], ...updates };
    // return Promise.resolve(this.customers[index]);
    throw new Error("Not implemented");
  }

  async delete(id: string): Promise<void> {
    // const index = this.customers.findIndex((c) => c.id === id);
    // if (index !== -1) {
    //   this.customers.splice(index, 1);
    // }
    // return Promise.resolve();
    throw new Error("Not implemented");
  }
}

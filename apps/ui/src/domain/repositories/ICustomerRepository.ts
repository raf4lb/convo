import { Customer } from "../entities/Customer";

export interface ICustomerRepository {
  getById(id: string): Promise<Customer | null>;
  getByCompanyId(companyId: string): Promise<Customer[]>;
  getByPhone(phone: string, companyId: string): Promise<Customer | null>;
  search(companyId: string, query: string): Promise<Customer[]>;
  create(
    companyId: string,
    name: string,
    phone: string,
    email: string | null,
    tags: string[],
    notes: string | null,
  ): Promise<Customer>;
  update(id: string, customer: Partial<Customer>): Promise<Customer>;
  delete(id: string): Promise<void>;
}

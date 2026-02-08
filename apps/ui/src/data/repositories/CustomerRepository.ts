import { Customer } from "../../domain/entities/Customer";
import { ICustomerRepository } from "../../domain/repositories/ICustomerRepository";

const mockCustomers: Customer[] = [
  {
    id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc085",
    companyId: "474d2fd7-2e99-452b-a4db-fe93ecf8729c",
    name: "Maria Silva",
    phone: "+55 11 98765-4321",
    email: "maria.silva@email.com",
    tags: ["VIP", "Cliente Recorrente"],
    notes: "Cliente muito importante, sempre compra produtos premium",
    createdAt: new Date("2024-01-10"),
    lastContactAt: new Date("2024-11-12T10:30:00"),
    isBlocked: false,
  },
  {
    id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc086",
    companyId: "474d2fd7-2e99-452b-a4db-fe93ecf8729c",
    name: "Carlos Santos",
    phone: "+55 21 99876-5432",
    email: "carlos.santos@email.com",
    tags: ["Novo Cliente"],
    notes: null,
    createdAt: new Date("2024-02-15"),
    lastContactAt: new Date("2024-11-12T09:15:00"),
    isBlocked: false,
  },
  {
    id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc087",
    companyId: "474d2fd7-2e99-452b-a4db-fe93ecf8729c",
    name: "Fernanda Lima",
    phone: "+55 11 91234-5678",
    email: null,
    tags: ["Interessado"],
    notes: null,
    createdAt: new Date("2024-03-20"),
    lastContactAt: new Date("2024-11-11T14:20:00"),
    isBlocked: false,
  },
  {
    id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc088",
    companyId: "474d2fd7-2e99-452b-a4db-fe93ecf8729c",
    name: "Pedro Oliveira",
    phone: "+55 11 98888-7777",
    email: "pedro.oliveira@email.com",
    tags: [],
    notes: null,
    createdAt: new Date("2024-04-05"),
    lastContactAt: new Date("2024-11-11T16:45:00"),
    isBlocked: false,
  },
  {
    id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc089",
    companyId: "474d2fd7-2e99-452b-a4db-fe93ecf8729c",
    name: "Julia Costa",
    phone: "+55 21 97777-6666",
    email: "julia.costa@email.com",
    tags: ["Urgente"],
    notes: "Precisa de atendimento prioritário",
    createdAt: new Date("2024-05-12"),
    lastContactAt: new Date("2024-11-12T11:45:00"),
    isBlocked: false,
  },
  {
    id: "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc090",
    companyId: "6dfaada5-37b1-442d-a21b-b63edf12bbd0",
    name: "Antônio Alves",
    phone: "+55 11 95555-4444",
    email: "antonio.alves@email.com",
    tags: [],
    notes: null,
    createdAt: new Date("2024-02-25"),
    lastContactAt: new Date("2024-11-10T10:00:00"),
    isBlocked: false,
  },
];

export class CustomerRepository implements ICustomerRepository {
  private customers: Customer[] = [...mockCustomers];

  async getById(id: string): Promise<Customer | null> {
    const customer = this.customers.find((c) => c.id === id);
    return Promise.resolve(customer || null);
  }

  async getByCompanyId(companyId: string): Promise<Customer[]> {
    const customers = this.customers.filter((c) => c.companyId === companyId);
    return Promise.resolve(customers);
  }

  async getByPhone(phone: string, companyId: string): Promise<Customer | null> {
    const customer = this.customers.find((c) => c.phone === phone && c.companyId === companyId);
    return Promise.resolve(customer || null);
  }

  async search(companyId: string, query: string): Promise<Customer[]> {
    const lowerQuery = query.toLowerCase();
    const customers = this.customers.filter(
      (c) =>
        c.companyId === companyId &&
        (c.name.toLowerCase().includes(lowerQuery) ||
          c.phone.includes(query) ||
          c.email?.toLowerCase().includes(lowerQuery) ||
          c.tags?.some((tag) => tag.toLowerCase().includes(lowerQuery))),
    );
    return Promise.resolve(customers);
  }

  async create(companyId: string, name: string, email: string, phone: string): Promise<Customer> {
    const customer: Customer = {
      id: Date.now().toString(),
      name: name,
      email: email,
      phone: phone,
      tags: [],
      notes: "",
      companyId: companyId,
      lastContactAt: null,
      isBlocked: false,
      createdAt: new Date(),
    };
    this.customers.push(customer);
    return Promise.resolve(customer);
  }

  async update(id: string, updates: Partial<Customer>): Promise<Customer> {
    const index = this.customers.findIndex((c) => c.id === id);
    if (index === -1) {
      throw new Error("Customer not found");
    }
    this.customers[index] = { ...this.customers[index], ...updates };
    return Promise.resolve(this.customers[index]);
  }

  async delete(id: string): Promise<void> {
    const index = this.customers.findIndex((c) => c.id === id);
    if (index !== -1) {
      this.customers.splice(index, 1);
    }
    return Promise.resolve();
  }
}

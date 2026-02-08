import { Customer } from "../../entities/Customer";
import { ICustomerRepository } from "../../repositories/ICustomerRepository";

export class CreateCustomer {
  constructor(private customerRepository: ICustomerRepository) {}

  async execute(
    companyId: string,
    name: string,
    phone: string,
    email: string | null,
    tags: string[],
    notes: string | null,
  ): Promise<Customer> {
    // Validate data
    if (!name || name.trim().length < 2) {
      throw new Error("Nome deve ter no mínimo 2 caracteres");
    }

    if (!phone || phone.trim().length < 10) {
      throw new Error("Telefone inválido");
    }

    // Check if phone already exists for this company
    const existingCustomer = await this.customerRepository.getByPhone(phone, companyId);
    if (existingCustomer) {
      throw new Error("Cliente com este telefone já cadastrado");
    }

    // Create customer
    const customer = await this.customerRepository.create(
      companyId,
      name,
      phone,
      email,
      tags,
      notes,
    );

    return customer;
  }
}

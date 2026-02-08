import { Customer } from "../../entities/Customer";
import { ICustomerRepository } from "../../repositories/ICustomerRepository";

export class SearchCustomers {
  constructor(private customerRepository: ICustomerRepository) {}

  async execute(companyId: string, query: string): Promise<Customer[]> {
    if (!query || query.trim().length === 0) {
      return await this.customerRepository.getByCompanyId(companyId);
    }

    return await this.customerRepository.search(companyId, query.trim());
  }
}

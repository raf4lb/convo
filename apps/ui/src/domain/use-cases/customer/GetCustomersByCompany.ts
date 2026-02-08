import { Customer } from "../../entities/Customer";
import { ICustomerRepository } from "../../repositories/ICustomerRepository";

export class GetCustomersByCompany {
  constructor(private customerRepository: ICustomerRepository) {}

  async execute(companyId: string): Promise<Customer[]> {
    return await this.customerRepository.getByCompanyId(companyId);
  }
}

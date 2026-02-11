import { AuthUser, UserRole } from "../../entities/User";
import { IUserRepository } from "../../repositories/IUserRepository";

export class SearchUsers {
  constructor(private userRepository: IUserRepository) {}

  async execute(companyId: string, query: string, roleFilter?: UserRole): Promise<AuthUser[]> {
    return await this.userRepository.getByCompanyId(companyId, roleFilter, query);
  }
}

import { AuthUser, UserRole } from "../../entities/User";
import { IUserRepository } from "../../repositories/IUserRepository";

export class SearchUsers {
  constructor(private userRepository: IUserRepository) {}

  async execute(companyId: string, query: string, roleFilter?: UserRole): Promise<AuthUser[]> {
    let users = await this.userRepository.getByCompanyId(companyId);

    // Filter by search query
    if (query && query.trim().length > 0) {
      const lowerQuery = query.toLowerCase().trim();
      users = users.filter(
        (user) =>
          user.name.toLowerCase().includes(lowerQuery) ||
          user.email.toLowerCase().includes(lowerQuery),
      );
    }

    // Filter by role
    if (roleFilter) {
      users = users.filter((user) => user.role === roleFilter);
    }

    return users;
  }
}

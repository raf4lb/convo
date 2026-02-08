import { Permission, RolePermissions } from "../../entities/Permission";
import { AuthUser, UserRole } from "../../entities/User";
import { IUserRepository } from "../../repositories/IUserRepository";

export class GetUsersByCompany {
  constructor(private userRepository: IUserRepository) {}

  async execute(companyId: string, userRole: UserRole): Promise<AuthUser[]> {
    // Check permission
    const permissions = RolePermissions[userRole];
    if (!permissions.includes(Permission.VIEW_USERS)) {
      throw new Error("Sem permissão para visualizar usuários");
    }

    return await this.userRepository.getByCompanyId(companyId);
  }
}

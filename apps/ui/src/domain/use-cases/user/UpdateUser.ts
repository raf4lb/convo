import { Permission, RolePermissions } from "../../entities/Permission";
import { AuthUser, User, UserRole } from "../../entities/User";
import { IUserRepository } from "../../repositories/IUserRepository";

export class UpdateUser {
  constructor(private userRepository: IUserRepository) {}

  async execute(userId: string, updates: Partial<User>, updaterRole: UserRole): Promise<AuthUser> {
    // Get user to update
    const userToUpdate = await this.userRepository.getById(userId);
    if (!userToUpdate) {
      throw new Error("Usuário não encontrado");
    }

    // Validate permissions
    this.validatePermissions(userToUpdate.role, updaterRole);

    // Validate data if changing role
    if (updates.role && updates.role !== userToUpdate.role) {
      this.validatePermissions(updates.role, updaterRole);
    }

    // Update user
    return await this.userRepository.update(userId, updates);
  }

  private validatePermissions(targetRole: UserRole, updaterRole: UserRole): void {
    const permissions = RolePermissions[updaterRole];

    if (
      targetRole === UserRole.ADMINISTRATOR &&
      !permissions.includes(Permission.CREATE_ADMINISTRATOR)
    ) {
      throw new Error("Sem permissão para editar administradores");
    }

    if (targetRole === UserRole.MANAGER && !permissions.includes(Permission.CREATE_MANAGER)) {
      throw new Error("Sem permissão para editar gerentes");
    }

    if (targetRole === UserRole.ATTENDANT && !permissions.includes(Permission.CREATE_ATTENDANT)) {
      throw new Error("Sem permissão para editar atendentes");
    }
  }
}

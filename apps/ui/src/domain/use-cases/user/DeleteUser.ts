import { Permission, RolePermissions } from "../../entities/Permission";
import { UserRole } from "../../entities/User";
import { IUserRepository } from "../../repositories/IUserRepository";

export class DeleteUser {
  constructor(private userRepository: IUserRepository) {}

  async execute(userId: string, deleterRole: UserRole): Promise<void> {
    // Get user to delete
    const userToDelete = await this.userRepository.getById(userId);
    if (!userToDelete) {
      throw new Error("Usuário não encontrado");
    }

    // Validate permissions
    this.validatePermissions(userToDelete.role, deleterRole);

    // Delete user
    await this.userRepository.delete(userId);
  }

  private validatePermissions(targetRole: UserRole, deleterRole: UserRole): void {
    const permissions = RolePermissions[deleterRole];

    if (
      targetRole === UserRole.ADMINISTRATOR &&
      !permissions.includes(Permission.CREATE_ADMINISTRATOR)
    ) {
      throw new Error("Sem permissão para deletar administradores");
    }

    if (targetRole === UserRole.MANAGER && !permissions.includes(Permission.CREATE_MANAGER)) {
      throw new Error("Sem permissão para deletar gerentes");
    }

    if (targetRole === UserRole.ATTENDANT && !permissions.includes(Permission.CREATE_ATTENDANT)) {
      throw new Error("Sem permissão para deletar atendentes");
    }
  }
}

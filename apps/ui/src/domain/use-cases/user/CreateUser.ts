import { Permission, RolePermissions } from "../../entities/Permission";
import { AuthUser, UserRole } from "../../entities/User";
import { IUserRepository } from "../../repositories/IUserRepository";

export class CreateUser {
  constructor(private userRepository: IUserRepository) {}

  async execute(
    data: {
      companyId: string;
      name: string;
      email: string;
      password: string;
      role: UserRole;
    },
    creatorRole: UserRole,
  ): Promise<AuthUser> {
    // Validate permissions
    this.validatePermissions(data.role, creatorRole);

    // Validate data
    if (!data.name || data.name.trim().length < 3) {
      throw new Error("Nome deve ter no mínimo 3 caracteres");
    }

    if (!data.email || !data.email.includes("@")) {
      throw new Error("Email inválido");
    }

    if (!data.password || data.password.length < 6) {
      throw new Error("Senha deve ter no mínimo 6 caracteres");
    }

    // Check if email already exists
    const existingUser = await this.userRepository.getByEmail(data.email);
    if (existingUser) {
      throw new Error("Email já cadastrado");
    }

    // Create user
    return await this.userRepository.create({
      companyId: data.companyId,
      name: data.name,
      email: data.email,
      password: data.password, // In production, hash this
      role: data.role,
      isActive: true,
    });
  }

  private validatePermissions(targetRole: UserRole, creatorRole: UserRole): void {
    const permissions = RolePermissions[creatorRole];

    if (
      targetRole === UserRole.ADMINISTRATOR &&
      !permissions.includes(Permission.CREATE_ADMINISTRATOR)
    ) {
      throw new Error("Sem permissão para criar administradores");
    }

    if (targetRole === UserRole.MANAGER && !permissions.includes(Permission.CREATE_MANAGER)) {
      throw new Error("Sem permissão para criar gerentes");
    }

    if (targetRole === UserRole.ATTENDANT && !permissions.includes(Permission.CREATE_ATTENDANT)) {
      throw new Error("Sem permissão para criar atendentes");
    }
  }
}

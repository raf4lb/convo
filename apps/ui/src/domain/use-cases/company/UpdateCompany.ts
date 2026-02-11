import {Company} from "../../entities/Company";
import {Permission, RolePermissions} from "../../entities/Permission";
import {UserRole} from "../../entities/User";
import {ICompanyRepository} from "../../repositories/ICompanyRepository";

export class UpdateCompany {
  constructor(private readonly companyRepository: ICompanyRepository) {}
  async execute(
    companyId: string,
    name: string,
    email: string,
    phone: string,
    whatsappApiKey: string | null,
    attendantSeesAllConversations: boolean,
    updaterRole: UserRole,
  ): Promise<Company> {
    const companyToUpdate = await this.companyRepository.getById(companyId);
    if (!companyToUpdate) {
      throw new Error("Empresa não encontrada");
    }

    this.validatePermissions(updaterRole);

    return await this.companyRepository.update(
        companyId,
        name,
        email,
        phone,
        whatsappApiKey,
        attendantSeesAllConversations,
    );
  }

  private validatePermissions(updaterRole: UserRole): void {
    const permissions = RolePermissions[updaterRole];
    if (!permissions.includes(Permission.UPDATE_COMPANY)) {
      throw new Error("Sem permissão para editar a empresa");
    }
  }
}

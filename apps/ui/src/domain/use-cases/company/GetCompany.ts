import { Company } from "../../entities/Company";
import { Permission, RolePermissions } from "../../entities/Permission";
import { UserRole } from "../../entities/User";
import { ICompanyRepository } from "../../repositories/ICompanyRepository";

export class GetCompany {
  constructor(private readonly companyRepository: ICompanyRepository) {}
  async execute(companyId: string, userRole: UserRole): Promise<Company> {
    const company = await this.companyRepository.getById(companyId);
    if (!company) {
      throw new Error("Empresa não encontrado");
    }

    this.validatePermissions(userRole);

    return company;
  }

  private validatePermissions(userRole: UserRole): void {
    const permissions = RolePermissions[userRole];
    if (!permissions.includes(Permission.VIEW_COMPANY)) {
      throw new Error("Sem permissão para visualizar empresa");
    }
  }
}

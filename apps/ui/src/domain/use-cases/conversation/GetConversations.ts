import { Conversation } from "../../entities/Conversation";
import { AuthUser, UserRole } from "../../entities/User";
import { ICompanyRepository } from "../../repositories/ICompanyRepository";
import { IConversationRepository } from "../../repositories/IConversationRepository";

export class GetConversations {
  constructor(
    private readonly conversationRepository: IConversationRepository,
    private readonly companyRepository: ICompanyRepository,
  ) {}

  async execute(user: AuthUser): Promise<Conversation[]> {
    const company = await this.companyRepository.getById(user.companyId);

    if (!company) throw new Error("Company not found");

    if (!company.attendantSeesAllConversations && user.role == UserRole.ATTENDANT) {
      return await this.conversationRepository.getByAttendant(user);
    }

    return await this.conversationRepository.getAll(user.companyId);
  }
}

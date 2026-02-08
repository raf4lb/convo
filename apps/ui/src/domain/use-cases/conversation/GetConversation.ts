import { Conversation } from "../../entities/Conversation";
import { AuthUser, UserRole } from "../../entities/User";
import { ICompanyRepository } from "../../repositories/ICompanyRepository";
import { IConversationRepository } from "../../repositories/IConversationRepository";

export class GetConversation {
  constructor(
    private readonly conversationRepository: IConversationRepository,
    private readonly companyRepository: ICompanyRepository,
  ) {}

  async execute(conversationId: string, user: AuthUser): Promise<Conversation | null> {
    const conversation = await this.conversationRepository.getById(user.companyId, conversationId);
    if (!conversation) throw new Error("Conversation not found");

    const company = await this.companyRepository.getById(conversation.companyId);
    if (!company) throw new Error("Company not found");

    if (
      !company.attendantSeesAllConversations &&
      conversation.assignedToUserId &&
      user.role == UserRole.ATTENDANT &&
      conversation.assignedToUserId != user.id
    ) {
      return null;
    }

    return conversation;
  }
}

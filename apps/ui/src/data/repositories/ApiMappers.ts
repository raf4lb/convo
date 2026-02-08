import { Company } from "../../domain/entities/Company";
import { Customer } from "../../domain/entities/Customer";
import { AuthUser, User, UserRole } from "../../domain/entities/User";

export interface CompanyDTO {
  id: string;
  name: string;
  email: string;
  phone: string;
  whatsapp_api_key: string | null;
  is_active: boolean;
  attendant_sees_all_conversations: boolean;
  created_at: string;
  updated_at: string | null;
}

export function mapToCompany(dto: CompanyDTO): Company {
  // TODO: data validation
  return {
    id: dto.id,
    name: dto.name,
    email: dto.email,
    phone: dto.phone,
    whatsappApiKey: dto.whatsapp_api_key,
    createdAt: new Date(dto.created_at),
    isActive: dto.is_active,
    attendantSeesAllConversations: dto.attendant_sees_all_conversations,
  };
}

export function mapToCompanyDTO(company: Company): CompanyDTO {
  // TODO: data validation
  return {
    id: company.id,
    name: company.name,
    email: company.email,
    phone: company.phone,
    whatsapp_api_key: company.whatsappApiKey,
    is_active: company.isActive,
    attendant_sees_all_conversations: company.attendantSeesAllConversations,
    created_at: company.createdAt.toISOString(),
    updated_at: null,
  };
}

export interface CustomerDTO {
  id: string;
  name: string;
  phone_number: string;
  email: string | null;
  company_id: string;
  is_blocked: boolean;
  tags: string[];
  notes: string | null;
  last_contact_at: string;
  created_at: string;
  updated_at: string | null;
}

export function mapToCustomer(dto: CustomerDTO): Customer {
  // TODO: data validation
  return {
    id: dto.id,
    companyId: dto.name,
    name: dto.name,
    phone: dto.phone_number,
    email: dto.email,
    tags: dto.tags,
    notes: dto.notes,
    createdAt: new Date(dto.created_at),
    lastContactAt: dto.last_contact_at ? new Date(dto.last_contact_at) : null,
    isBlocked: dto.is_blocked,
  };
}

export interface UserDTO {
  id: string;
  name: string;
  email: string;
  company_id: string;
  type: "administrator" | "manager" | "staff";
  is_active: boolean;
  created_at: string;
  updated_at: string | null;
}

export function mapBackendTypeToRole(type: "administrator" | "manager" | "staff"): UserRole {
  const mapping = {
    administrator: UserRole.ADMINISTRATOR,
    manager: UserRole.MANAGER,
    staff: UserRole.ATTENDANT,
  };
  return mapping[type];
}

function mapRoleToBackendType(role: UserRole): "administrator" | "manager" | "staff" {
  const mapping = {
    [UserRole.ADMINISTRATOR]: "administrator" as const,
    [UserRole.MANAGER]: "manager" as const,
    [UserRole.ATTENDANT]: "staff" as const,
  };
  return mapping[role];
}

export function mapToUser(dto: UserDTO): User {
  // TODO: data validation
  return {
    id: dto.id,
    companyId: dto.company_id,
    name: dto.name,
    email: dto.email,
    password: "", // Backend never returns password for security
    role: mapBackendTypeToRole(dto.type),
    isActive: dto.is_active,
    createdAt: new Date(dto.created_at),
    lastLoginAt: undefined, // Backend doesn't track this yet
  };
}

export function mapToAuthUser(dto: UserDTO): AuthUser {
  const user = mapToUser(dto);
  const { password: _, ...authUser } = user;
  return authUser;
}

export { mapRoleToBackendType };

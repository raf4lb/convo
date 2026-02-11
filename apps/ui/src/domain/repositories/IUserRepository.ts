import { AuthUser, User, UserRole } from "../entities/User";

export interface IUserRepository {
  getById(id: string): Promise<User | null>;
  getByEmail(companyId: string, email: string): Promise<User | null>;
  getByCompanyId(companyId: string, role?: UserRole, search?: string): Promise<AuthUser[]>;
  create(user: Omit<User, "id" | "createdAt">): Promise<AuthUser>;
  update(id: string, user: Partial<User>): Promise<AuthUser>;
  delete(id: string): Promise<void>;
  updateLastLogin(id: string): Promise<void>;
}

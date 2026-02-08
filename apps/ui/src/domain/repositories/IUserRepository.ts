import { AuthUser, User } from "../entities/User";

export interface IUserRepository {
  getById(id: string): Promise<User | null>;
  getByEmail(email: string): Promise<User | null>;
  getByCompanyId(companyId: string): Promise<AuthUser[]>;
  create(user: Omit<User, "id" | "createdAt">): Promise<AuthUser>;
  update(id: string, user: Partial<User>): Promise<AuthUser>;
  delete(id: string): Promise<void>;
  updateLastLogin(id: string): Promise<void>;
}

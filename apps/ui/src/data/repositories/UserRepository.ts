import { AuthUser, User, UserRole } from "@/domain/entities/User";
import { IUserRepository } from "@/domain/repositories/IUserRepository";

const mockUsers: User[] = [
  {
    id: "03f1d919-cba6-479f-baec-5fcbc77b9d85",
    companyId: "474d2fd7-2e99-452b-a4db-fe93ecf8729c",
    name: "Admin User",
    email: "admin@techsolutions.com",
    password: "123456", // In production, this should be hashed
    role: UserRole.ADMINISTRATOR,
    isActive: true,
    createdAt: new Date("2024-01-15"),
  },
  {
    id: "e8bf801b-d16a-4736-8df9-df9d9278293c",
    companyId: "474d2fd7-2e99-452b-a4db-fe93ecf8729c",
    name: "João Silva",
    email: "joao@techsolutions.com",
    password: "123456",
    role: UserRole.ATTENDANT,
    isActive: true,
    createdAt: new Date("2024-01-20"),
  },
  {
    id: "3b757f19-4cba-448a-b114-31d54c53adf9",
    companyId: "474d2fd7-2e99-452b-a4db-fe93ecf8729c",
    name: "Ana Costa",
    email: "ana@techsolutions.com",
    password: "123456",
    role: UserRole.ATTENDANT,
    isActive: true,
    createdAt: new Date("2024-01-20"),
  },
  {
    id: "23d04704-3770-4e4e-b5fe-b73359a400f5",
    companyId: "474d2fd7-2e99-452b-a4db-fe93ecf8729c",
    name: "Carlos Mendes",
    email: "carlos@techsolutions.com",
    password: "123456",
    role: UserRole.MANAGER,
    isActive: true,
    createdAt: new Date("2024-01-18"),
  },
  {
    id: "b7b5c158-355d-45c2-b021-7e1bdbdd0f87",
    companyId: "6dfaada5-37b1-442d-a21b-b63edf12bbd0",
    name: "Admin Comércio",
    email: "admin@comerciodigital.com",
    password: "123456",
    role: UserRole.ADMINISTRATOR,
    isActive: true,
    createdAt: new Date("2024-02-20"),
  },
];

export class UserRepository implements IUserRepository {
  private users: User[] = [...mockUsers];

  async getById(id: string): Promise<User | null> {
    const user = this.users.find((u) => u.id === id);
    return Promise.resolve(user || null);
  }

  async getByEmail(email: string): Promise<User | null> {
    const user = this.users.find((u) => u.email === email);
    return Promise.resolve(user || null);
  }

  async getByCompanyId(companyId: string): Promise<AuthUser[]> {
    const users = this.users.filter((u) => u.companyId === companyId).map(this.removePassword);
    return Promise.resolve(users);
  }

  async create(data: Omit<User, "id" | "createdAt">): Promise<AuthUser> {
    const user: User = {
      ...data,
      id: Date.now().toString(),
      createdAt: new Date(),
    };
    this.users.push(user);
    return Promise.resolve(this.removePassword(user));
  }

  async update(id: string, updates: Partial<User>): Promise<AuthUser> {
    const index = this.users.findIndex((u) => u.id === id);
    if (index === -1) {
      throw new Error("User not found");
    }
    this.users[index] = { ...this.users[index], ...updates };
    return Promise.resolve(this.removePassword(this.users[index]));
  }

  async delete(id: string): Promise<void> {
    const index = this.users.findIndex((u) => u.id === id);
    if (index !== -1) {
      this.users.splice(index, 1);
    }
    return Promise.resolve();
  }

  async updateLastLogin(id: string): Promise<void> {
    const index = this.users.findIndex((u) => u.id === id);
    if (index !== -1) {
      this.users[index].lastLoginAt = new Date();
    }
    return Promise.resolve();
  }

  private removePassword(user: User): AuthUser {
    const { password: _, ...authUser } = user;
    return authUser;
  }
}

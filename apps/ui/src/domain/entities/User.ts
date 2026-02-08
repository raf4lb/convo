export enum UserRole {
  ADMINISTRATOR = "ADMINISTRATOR",
  MANAGER = "MANAGER",
  ATTENDANT = "ATTENDANT",
}

export interface User {
  id: string;
  companyId: string;
  name: string;
  email: string;
  password: string; // In production, this should be hashed
  role: UserRole;
  isActive: boolean;
  createdAt: Date;
  lastLoginAt?: Date;
}

export type AuthUser = Omit<User, "password">;

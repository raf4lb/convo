import { AuthSession } from "../../domain/entities/AuthSession";
import { IAuthRepository } from "../../domain/repositories/IAuthRepository";
import { ICompanyRepository } from "../../domain/repositories/ICompanyRepository";
import { IUserRepository } from "../../domain/repositories/IUserRepository";

// Simple in-memory session storage
const sessions = new Map<string, AuthSession>();

export class AuthRepository implements IAuthRepository {
  constructor(
    private userRepository: IUserRepository,
    private companyRepository: ICompanyRepository,
  ) {}

  async authenticate(email: string, password: string): Promise<AuthSession | null> {
    // Find user by email
    const user = await this.userRepository.getByEmail(email);

    if (!user) {
      return null;
    }

    // In production, compare hashed passwords
    if (user.password !== password) {
      return null;
    }

    // Get company
    const company = await this.companyRepository.getById(user.companyId);

    if (!company) {
      return null;
    }

    // Update last login
    await this.userRepository.updateLastLogin(user.id);

    // Create session
    const token = this.generateToken();
    const expiresAt = new Date();
    expiresAt.setHours(expiresAt.getHours() + 24); // 24 hours

    const { password: _, ...authUser } = user;

    const session: AuthSession = {
      user: authUser,
      company,
      token,
      expiresAt,
    };

    // Store session
    sessions.set(token, session);

    return session;
  }

  async validateToken(token: string): Promise<AuthSession | null> {
    const session = sessions.get(token);

    if (!session) {
      return null;
    }

    // Check if expired
    if (session.expiresAt < new Date()) {
      sessions.delete(token);
      return null;
    }

    return session;
  }

  async logout(token: string): Promise<void> {
    sessions.delete(token);
    return Promise.resolve();
  }

  private generateToken(): string {
    return `token_${Date.now()}_${Math.random().toString(36).substring(2)}`;
  }
}

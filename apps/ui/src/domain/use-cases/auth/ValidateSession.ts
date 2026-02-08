import { AuthSession } from "../../entities/AuthSession";
import { IAuthRepository } from "../../repositories/IAuthRepository";

export class ValidateSession {
  constructor(private authRepository: IAuthRepository) {}

  async execute(token: string): Promise<AuthSession | null> {
    // Token parameter kept for backwards compatibility but not used with cookie-based auth
    // The actual JWT is in httpOnly cookies and sent automatically by the browser
    const session = await this.authRepository.validateToken(token);

    if (!session) {
      return null;
    }

    // Check if token is expired
    if (session.expiresAt < new Date()) {
      return null;
    }

    return session;
  }
}

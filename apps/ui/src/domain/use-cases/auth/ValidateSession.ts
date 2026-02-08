import { AuthSession } from "../../entities/AuthSession";
import { IAuthRepository } from "../../repositories/IAuthRepository";

export class ValidateSession {
  constructor(private authRepository: IAuthRepository) {}

  async execute(token: string): Promise<AuthSession | null> {
    if (!token) {
      return null;
    }

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

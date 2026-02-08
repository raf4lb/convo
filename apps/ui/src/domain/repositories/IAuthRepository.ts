import { AuthSession } from "../entities/AuthSession";

export interface IAuthRepository {
  authenticate(email: string, password: string): Promise<AuthSession | null>;
  validateToken(token: string): Promise<AuthSession | null>;
  logout(token: string): Promise<void>;
}

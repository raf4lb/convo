import { AuthSession } from "../../entities/AuthSession";
import { IWebSocketAdapter } from "../../ports/IWebSocketAdapter";
import { IAuthRepository } from "../../repositories/IAuthRepository";

export class Login {
  constructor(
    private readonly authRepository: IAuthRepository,
    private readonly messagesWebSocket: IWebSocketAdapter,
  ) {}

  async execute(email: string, password: string): Promise<AuthSession> {
    // Validations
    if (!email || !email.includes("@")) {
      throw new Error("Email inválido");
    }

    if (!password || password.length < 6) {
      throw new Error("Senha deve ter no mínimo 6 caracteres");
    }

    // Authenticate
    const session = await this.authRepository.authenticate(email, password);

    if (!session) {
      throw new Error("Credenciais inválidas");
    }

    if (!session.user.isActive) {
      throw new Error("Usuário desativado");
    }

    if (!session.company.isActive) {
      throw new Error("Empresa desativada");
    }

    this.messagesWebSocket.connect();

    return session;
  }
}

import { IWebSocketAdapter } from "../../ports/IWebSocketAdapter";
import { IAuthRepository } from "../../repositories/IAuthRepository";

export class Logout {
  constructor(
    private authRepository: IAuthRepository,
    private readonly messagesWebSocket: IWebSocketAdapter,
  ) {}

  async execute(token: string): Promise<void> {
    await this.authRepository.logout(token);
    this.messagesWebSocket.disconnect();
  }
}

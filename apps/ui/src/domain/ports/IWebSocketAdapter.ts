export type OnMessageHandler = (data: any) => Promise<void>;

export interface IWebSocketAdapter {
  connect: () => void;
  disconnect: () => void;
  send: (data: string) => void;
  /**
   * Registers a handler that will be called whenever a new message arrives.
   * Returns an unsubscribe function.
   */
  addHandler: (handler: OnMessageHandler) => () => void;
}

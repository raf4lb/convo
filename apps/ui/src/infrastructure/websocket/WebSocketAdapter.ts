import {
  ConnectionState,
  IWebSocketAdapter,
  OnMessageHandler,
} from "@/domain/ports/IWebSocketAdapter";

export class WebSocketAdapter implements IWebSocketAdapter {
  private socket?: WebSocket;
  private handlers = new Set<OnMessageHandler>();
  private state: ConnectionState = ConnectionState.DISCONNECTED;
  private reconnectAttempts = 0;
  private reconnectTimeout?: NodeJS.Timeout;
  private shouldReconnect = true;

  constructor(
    private url: string,
    private maxReconnectAttempts: number = 3,
    private baseBackoffMs: number = 100,
  ) {}

  getState(): ConnectionState {
    return this.state;
  }

  private setState(newState: ConnectionState): void {
    this.state = newState;
    console.log(`[WebSocketAdapter] state changed to ${newState}`);
  }

  private scheduleReconnect(): void {
    // Exponential backoff: 100ms, 200ms, 400ms, 800ms, 1600ms, capped at 5000ms
    const backoffMs = Math.min(this.baseBackoffMs * Math.pow(2, this.reconnectAttempts), 5000);

    console.log(
      `[WebSocketAdapter] reconnecting in ${backoffMs}ms (attempt ${this.reconnectAttempts + 1}/${this.maxReconnectAttempts})`,
    );

    this.reconnectTimeout = setTimeout(() => {
      this.reconnectAttempts++;
      this.connect();
    }, backoffMs);
  }

  private cancelReconnect(): void {
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = undefined;
    }
  }

  connect(): void {
    // Prevent duplicate connections
    if (
      this.socket &&
      (this.socket.readyState === WebSocket.OPEN || this.socket.readyState === WebSocket.CONNECTING)
    ) {
      return;
    }

    this.setState(ConnectionState.CONNECTING);
    this.shouldReconnect = true; // Enable reconnection on connect

    try {
      this.socket = new WebSocket(this.url);

      this.socket.onopen = () => {
        console.log("[WebSocketAdapter] connected", this.url);
        this.setState(ConnectionState.CONNECTED);
        this.reconnectAttempts = 0; // Reset on successful connection
      };

      this.socket.onmessage = (ev) => {
        try {
          const data = JSON.parse(ev.data);
          if (!data || typeof data.text !== "string") {
            console.warn("[WebSocketAdapter] invalid payload", data);
            return;
          }
          this.handlers.forEach((h) => {
            try {
              h(data);
            } catch (err) {
              console.error("handler error", err);
            }
          });
        } catch (err) {
          console.error("[WebSocketAdapter] parse error", err);
        }
      };

      this.socket.onclose = (ev) => {
        console.log("[WebSocketAdapter] closed", ev.code, ev.reason);

        // Only reconnect on abnormal closures and if not intentionally disconnected
        const isAbnormalClosure = ev.code !== 1000 && ev.code !== 1001;

        if (isAbnormalClosure && this.shouldReconnect) {
          if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.setState(ConnectionState.RECONNECTING);
            this.scheduleReconnect();
          } else {
            console.error("[WebSocketAdapter] max reconnection attempts reached");
            this.setState(ConnectionState.ERROR);
          }
        } else {
          this.setState(ConnectionState.DISCONNECTED);
        }
      };

      this.socket.onerror = (err) => {
        console.error("[WebSocketAdapter] error", err);
      };
    } catch (error) {
      console.error("[WebSocketAdapter] connection error", error);
      this.setState(ConnectionState.ERROR);
    }
  }

  disconnect(): void {
    this.shouldReconnect = false; // Disable reconnection on intentional disconnect
    this.cancelReconnect();
    this.socket?.close(1000, "intentional disconnect"); // Normal closure code
    this.socket = undefined;
    this.setState(ConnectionState.DISCONNECTED);
    // Note: Don't clear handlers - they should persist across reconnections
  }

  send(data: string): void {
    this.socket?.send(data);
  }

  /**
   * Registers a handler that will be called whenever a new message arrives.
   * Returns an unsubscribe function.
   */
  addHandler(handler: OnMessageHandler): () => void {
    this.handlers.add(handler);
    return () => this.handlers.delete(handler);
  }
}

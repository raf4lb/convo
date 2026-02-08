// src/infra/websocket/WebSocketAdapter.ts

import { IWebSocketAdapter, OnMessageHandler } from "../../domain/ports/IWebSocketAdapter";

export class WebSocketAdapter implements IWebSocketAdapter {
  private socket?: WebSocket;
  private handlers = new Set<OnMessageHandler>();

  constructor(private url: string) {}

  connect(): void {
    if (
      this.socket &&
      (this.socket.readyState === WebSocket.OPEN || this.socket.readyState === WebSocket.CONNECTING)
    ) {
      return;
    }

    this.socket = new WebSocket(this.url);

    this.socket.onopen = () => {
      console.log("[WebSocketAdapter] connected", this.url);
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
    };

    this.socket.onerror = (err) => {
      console.error("[WebSocketAdapter] error", err);
    };
  }

  disconnect(): void {
    this.socket?.close();
    this.socket = undefined;
    this.handlers.clear();
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

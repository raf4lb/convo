import { useEffect, useState } from "react";

import { ConnectionState } from "@/domain/ports/IWebSocketAdapter";
import { messagesWebSocket } from "@/infrastructure/di/container";

export function useConnectionStatus() {
  const [state, setState] = useState<ConnectionState>(messagesWebSocket.getState());

  useEffect(() => {
    // Poll connection state every second
    const interval = setInterval(() => {
      setState(messagesWebSocket.getState());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return state;
}

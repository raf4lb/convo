import { Wifi, WifiOff, Loader2, AlertCircle } from "lucide-react";

import { useConnectionStatus } from "../hooks/useConnectionStatus";

import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { ConnectionState } from "@/domain/ports/IWebSocketAdapter";

export function ConnectionStatus() {
  const state = useConnectionStatus();

  // Hide when connected (only show issues)
  if (state === ConnectionState.CONNECTED) {
    return null;
  }

  const config = {
    [ConnectionState.CONNECTING]: {
      icon: Loader2,
      label: "Conectando",
      className: "bg-blue-50 text-blue-700",
      animate: true,
    },
    [ConnectionState.RECONNECTING]: {
      icon: Loader2,
      label: "Reconectando",
      className: "bg-amber-50 text-amber-700",
      animate: true,
    },
    [ConnectionState.ERROR]: {
      icon: AlertCircle,
      label: "Sem conexão",
      className: "bg-red-50 text-red-700",
      animate: false,
    },
    [ConnectionState.DISCONNECTED]: {
      icon: WifiOff,
      label: "Desconectado",
      className: "bg-neutral-50 text-neutral-700",
      animate: false,
    },
    [ConnectionState.CONNECTED]: {
      icon: Wifi,
      label: "Conectado",
      className: "bg-green-50 text-green-700",
      animate: false,
    },
  };

  const { icon: Icon, label, className, animate } = config[state];

  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${className}`}>
          <Icon className={`w-4 h-4 ${animate ? "animate-spin" : ""}`} />
        </div>
      </TooltipTrigger>
      <TooltipContent side="right">
        <p>{label}</p>
      </TooltipContent>
    </Tooltip>
  );
}

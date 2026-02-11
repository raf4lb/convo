import { createContext } from "react";

import { AuthSession } from "@/domain/entities/AuthSession.ts";
import { Permission } from "@/domain/entities/Permission.ts";

export interface AuthContextType {
  session: AuthSession | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  hasPermission: (permission: Permission) => boolean;
  hasAnyPermission: (permissions: Permission[]) => boolean;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

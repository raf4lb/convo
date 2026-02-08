import { createContext, ReactNode, useContext, useEffect, useState } from "react";

import { AuthSession } from "../../domain/entities/AuthSession";
import { Permission } from "../../domain/entities/Permission";
import {
  checkPermissionUseCase,
  loginUseCase,
  logoutUseCase,
  validateSessionUseCase,
} from "../../infrastructure/di/container";

interface AuthContextType {
  session: AuthSession | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  hasPermission: (permission: Permission) => boolean;
  hasAnyPermission: (permissions: Permission[]) => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const TOKEN_KEY = "auth_token";

export function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<AuthSession | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    validateStoredSession();
  }, []);

  const validateStoredSession = async () => {
    try {
      const token = localStorage.getItem(TOKEN_KEY);
      if (token) {
        const validSession = await validateSessionUseCase.execute(token);
        if (validSession) {
          setSession(validSession);
        } else {
          localStorage.removeItem(TOKEN_KEY);
        }
      }
    } catch (error) {
      console.error("Error validating session:", error);
      localStorage.removeItem(TOKEN_KEY);
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    const newSession = await loginUseCase.execute(email, password);
    setSession(newSession);
    localStorage.setItem(TOKEN_KEY, newSession.token);
  };

  const logout = async () => {
    try {
      if (session) {
        await logoutUseCase.execute(session.token);
      }
      setSession(null);
      localStorage.removeItem(TOKEN_KEY);
    } catch (error) {
      console.error("Error logging out:", error);
    }
  };

  const hasPermission = (permission: Permission): boolean => {
    if (!session) return false;
    return checkPermissionUseCase.execute(session.user.role, permission);
  };

  const hasAnyPermission = (permissions: Permission[]): boolean => {
    if (!session) return false;
    return permissions.some((p) => hasPermission(p));
  };

  return (
    <AuthContext.Provider
      value={{ session, loading, login, logout, hasPermission, hasAnyPermission }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

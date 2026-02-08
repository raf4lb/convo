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

export function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<AuthSession | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    validateStoredSession();
  }, []);

  const validateStoredSession = async () => {
    try {
      const validSession = await validateSessionUseCase.execute("");
      if (validSession) {
        setSession(validSession);
      }
    } catch (error) {
      throw new Error("Error validating session: " + error.toString());
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    const newSession = await loginUseCase.execute(email, password);
    setSession(newSession);
  };

  const logout = async () => {
    try {
      await logoutUseCase.execute("");
      setSession(null);
    } catch (error) {
      throw new Error("Error logging out: " + error.toString());
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

import { ReactNode, useEffect, useState } from "react";

import { AuthContext } from "./authContextDefinition";

import { AuthSession } from "@/domain/entities/AuthSession.ts";
import { Permission } from "@/domain/entities/Permission.ts";
import {
  checkPermissionUseCase,
  loginUseCase,
  logoutUseCase,
  validateSessionUseCase,
} from "@/infrastructure/di/container.ts";

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

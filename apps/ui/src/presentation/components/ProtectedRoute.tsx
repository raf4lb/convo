import { ReactNode } from "react";

import { ShieldAlert } from "lucide-react";

import { Alert, AlertDescription } from "../../components/ui/alert";
import { Permission } from "../../domain/entities/Permission";
import { useAuth } from "../contexts/AuthContext";

interface ProtectedRouteProps {
  children: ReactNode;
  requiredPermission?: Permission;
  requiredPermissions?: Permission[];
  fallback?: ReactNode;
}

export function ProtectedRoute({
  children,
  requiredPermission,
  requiredPermissions,
  fallback,
}: ProtectedRouteProps) {
  const { hasPermission, hasAnyPermission } = useAuth();

  let hasAccess = true;

  if (requiredPermission) {
    hasAccess = hasPermission(requiredPermission);
  } else if (requiredPermissions) {
    hasAccess = hasAnyPermission(requiredPermissions);
  }

  if (!hasAccess) {
    if (fallback) {
      return <>{fallback}</>;
    }

    return (
      <div className="flex-1 flex items-center justify-center bg-neutral-50 p-6">
        <Alert className="max-w-md">
          <ShieldAlert className="h-4 w-4" />
          <AlertDescription>
            Você não tem permissão para acessar esta funcionalidade.
          </AlertDescription>
        </Alert>
      </div>
    );
  }

  return <>{children}</>;
}

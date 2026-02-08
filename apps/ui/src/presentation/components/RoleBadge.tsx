import { Shield, User, UserCog } from "lucide-react";

import { Badge } from "../../components/ui/badge";
import { UserRole } from "../../domain/entities/User";

interface RoleBadgeProps {
  role: UserRole;
  showIcon?: boolean;
}

export function RoleBadge({ role, showIcon = true }: RoleBadgeProps) {
  const config = {
    [UserRole.ADMINISTRATOR]: {
      label: "Administrador",
      icon: Shield,
      className: "bg-purple-50 text-purple-700 border-purple-200",
    },
    [UserRole.MANAGER]: {
      label: "Gerente",
      icon: UserCog,
      className: "bg-blue-50 text-blue-700 border-blue-200",
    },
    [UserRole.ATTENDANT]: {
      label: "Atendente",
      icon: User,
      className: "bg-green-50 text-green-700 border-green-200",
    },
  };

  const { label, icon: Icon, className } = config[role];

  return (
    <Badge variant="outline" className={className}>
      <span className="flex items-center gap-1">
        {showIcon && <Icon className="w-3 h-3" />}
        {label}
      </span>
    </Badge>
  );
}

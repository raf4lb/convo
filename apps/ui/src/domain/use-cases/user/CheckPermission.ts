import { Permission, RolePermissions } from "../../entities/Permission";
import { UserRole } from "../../entities/User";

export class CheckPermission {
  execute(userRole: UserRole, permission: Permission): boolean {
    const permissions = RolePermissions[userRole];
    return permissions.includes(permission);
  }

  executeMultiple(userRole: UserRole, requiredPermissions: Permission[]): boolean {
    const permissions = RolePermissions[userRole];
    return requiredPermissions.every((p) => permissions.includes(p));
  }
}

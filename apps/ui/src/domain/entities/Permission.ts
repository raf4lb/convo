import { UserRole } from "./User";

export enum Permission {
  // User Management
  CREATE_ADMINISTRATOR = "CREATE_ADMINISTRATOR",
  CREATE_MANAGER = "CREATE_MANAGER",
  CREATE_ATTENDANT = "CREATE_ATTENDANT",
  UPDATE_USER = "UPDATE_USER",
  DELETE_USER = "DELETE_USER",
  VIEW_USERS = "VIEW_USERS",

  // Conversation Management
  VIEW_CONVERSATIONS = "VIEW_CONVERSATIONS",
  ASSIGN_CONVERSATION = "ASSIGN_CONVERSATION",
  VIEW_ALL_CONVERSATIONS = "VIEW_ALL_CONVERSATIONS",

  // Customer Management
  VIEW_CUSTOMERS = "VIEW_CUSTOMERS",
  CREATE_CUSTOMER = "CREATE_CUSTOMER",
  UPDATE_CUSTOMER = "UPDATE_CUSTOMER",
  DELETE_CUSTOMER = "DELETE_CUSTOMER",

  // Company Management
  UPDATE_COMPANY = "UPDATE_COMPANY",
  VIEW_COMPANY = "VIEW_COMPANY",

  // Metrics
  VIEW_DASHBOARD = "VIEW_DASHBOARD",
  VIEW_ALL_METRICS = "VIEW_ALL_METRICS",
  VIEW_OWN_METRICS = "VIEW_OWN_METRICS",

  // Settings
  VIEW_SETTINGS = "VIEW_SETTINGS",
}

export const RolePermissions: Record<UserRole, Permission[]> = {
  [UserRole.ADMINISTRATOR]: [
    // Full access
    Permission.CREATE_ADMINISTRATOR,
    Permission.CREATE_MANAGER,
    Permission.CREATE_ATTENDANT,
    Permission.UPDATE_USER,
    Permission.DELETE_USER,
    Permission.VIEW_USERS,
    Permission.VIEW_CONVERSATIONS,
    Permission.ASSIGN_CONVERSATION,
    Permission.VIEW_ALL_CONVERSATIONS,
    Permission.VIEW_CUSTOMERS,
    Permission.CREATE_CUSTOMER,
    Permission.UPDATE_CUSTOMER,
    Permission.DELETE_CUSTOMER,
    Permission.UPDATE_COMPANY,
    Permission.VIEW_COMPANY,
    Permission.VIEW_DASHBOARD,
    Permission.VIEW_ALL_METRICS,
    Permission.VIEW_SETTINGS,
  ],
  [UserRole.MANAGER]: [
    Permission.CREATE_ATTENDANT,
    Permission.VIEW_USERS,
    Permission.VIEW_CONVERSATIONS,
    Permission.ASSIGN_CONVERSATION,
    Permission.VIEW_ALL_CONVERSATIONS,
    Permission.VIEW_CUSTOMERS,
    Permission.CREATE_CUSTOMER,
    Permission.UPDATE_CUSTOMER,
    Permission.VIEW_COMPANY,
    Permission.VIEW_DASHBOARD,
    Permission.VIEW_ALL_METRICS,
  ],
  [UserRole.ATTENDANT]: [
    Permission.VIEW_CONVERSATIONS,
    Permission.VIEW_CUSTOMERS,
    Permission.VIEW_COMPANY,
    Permission.VIEW_OWN_METRICS,
  ],
};

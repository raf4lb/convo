import { Company } from "./Company";
import { AuthUser } from "./User";

export interface AuthSession {
  user: AuthUser;
  company: Company;
  token: string;
  expiresAt: Date;
}

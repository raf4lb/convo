import { AuthSession } from "../../domain/entities/AuthSession";
import { IAuthRepository } from "../../domain/repositories/IAuthRepository";
import { ICompanyRepository } from "../../domain/repositories/ICompanyRepository";
import { HttpClient } from "../../infrastructure/http/HttpClient";

import { mapBackendTypeToRole } from "./ApiMappers";

export class AuthRepository implements IAuthRepository {
  constructor(
    private httpClient: HttpClient,
    private companyRepository: ICompanyRepository,
  ) {}

  async authenticate(email: string, password: string): Promise<AuthSession | null> {
    try {
      const response = await this.httpClient.post("/auth/login", {
        body: { email, password },
      });

      if (response.status !== 200) {
        return null;
      }

      const data = response.data as {
        user: {
          id: string;
          name: string;
          email: string;
          type: string;
          company_id: string;
          is_active: boolean;
        };
      };

      const company = await this.companyRepository.getById(data.user.company_id);

      if (!company) {
        return null;
      }

      const expiresAt = new Date();
      expiresAt.setMinutes(expiresAt.getMinutes() + 15); // 15 minutes (access token expiry)

      const session: AuthSession = {
        user: {
          id: data.user.id,
          companyId: data.user.company_id,
          name: data.user.name,
          email: data.user.email,
          role: mapBackendTypeToRole(data.user.type as "administrator" | "manager" | "staff"),
          isActive: data.user.is_active,
          createdAt: new Date(),
        },
        company,
        token: "", // Token is in httpOnly cookie
        expiresAt,
      };

      return session;
    } catch (error) {
      throw new Error("Authentication failed: " + error.toString());
    }
  }

  async validateToken(_token: string): Promise<AuthSession | null> {
    try {
      const response = await this.httpClient.get("/auth/me");

      if (response.status !== 200) {
        console.error("validateToken: /auth/me returned non-200 status:", response.status);
        return null;
      }

      const data = response.data as {
        id: string;
        name: string;
        email: string;
        type: string;
        company_id: string;
        is_active: boolean;
      };

      if (!data || !data.id) {
        throw new Error("validateToken: Invalid response data " + data);
      }

      const company = await this.companyRepository.getById(data.company_id);

      if (!company) {
        throw new Error("validateToken: Company not found for id: " + data.company_id);
      }

      const expiresAt = new Date();
      expiresAt.setMinutes(expiresAt.getMinutes() + 15);

      const session: AuthSession = {
        user: {
          id: data.id,
          companyId: data.company_id,
          name: data.name,
          email: data.email,
          role: mapBackendTypeToRole(data.type as "administrator" | "manager" | "staff"),
          isActive: data.is_active,
          createdAt: new Date(),
        },
        company,
        token: "",
        expiresAt,
      };

      return session;
    } catch (error) {
      throw new Error("Token validation failed: " + error.toString());
    }
  }

  async logout(_token: string): Promise<void> {
    try {
      await this.httpClient.post("/auth/logout");
    } catch (error) {
      throw new Error("Logout failed: " + error.toString());
    }
  }
}

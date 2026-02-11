import { UserDTO, mapToUser, mapToAuthUser, mapRoleToBackendType } from "./ApiMappers";

import { AuthUser, User } from "@/domain/entities/User";
import { IUserRepository } from "@/domain/repositories/IUserRepository";
import { HttpClient } from "@/infrastructure/http/HttpClient";

export class ApiUserRepository implements IUserRepository {
  constructor(private readonly client: HttpClient) {}

  async getById(id: string): Promise<User | null> {
    const path = `/users/${id}`;
    const res = await this.client.get(path);
    if (res.status === 404) return null;
    const body = res.data;
    return body ? mapToUser(body as UserDTO) : null;
  }

  async getByEmail(email: string): Promise<User | null> {
    // Workaround: Backend lacks GET /users/email/{email}
    // Fetch all users and filter client-side
    const path = "/users/";
    const res = await this.client.get(path);
    const body = res.data;

    if (!body || typeof body !== "object" || !("results" in body)) {
      throw new Error("Invalid API response");
    }

    const results = body.results;
    if (!Array.isArray(results)) {
      throw new Error("Invalid API response");
    }

    const users = results.map((dto: UserDTO) => mapToUser(dto));
    return users.find((user) => user.email === email) || null;
  }

  async getByCompanyId(companyId: string): Promise<AuthUser[]> {
    // Workaround: Backend lacks GET /users/company/{companyId}
    // Fetch all users and filter client-side
    const path = "/users/";
    const res = await this.client.get(path);
    const body = res.data;

    if (!body || typeof body !== "object" || !("results" in body)) {
      throw new Error("Invalid API response");
    }

    const results = body.results;
    if (!Array.isArray(results)) {
      throw new Error("Invalid API response");
    }

    return results
      .filter((dto: UserDTO) => dto.company_id === companyId)
      .map((dto: UserDTO) => mapToAuthUser(dto));
  }

  async create(data: Omit<User, "id" | "createdAt">): Promise<AuthUser> {
    const path = "/users/";
    const payload = {
      name: data.name,
      email: data.email,
      type: mapRoleToBackendType(data.role),
      company_id: data.companyId,
      is_active: data.isActive,
    };
    const res = await this.client.post(path, { body: payload });
    const body = res.data;
    return mapToAuthUser(body as UserDTO);
  }

  async update(id: string, updates: Partial<User>): Promise<AuthUser> {
    // Backend PUT requires full object, so fetch current user first
    const currentUser = await this.getById(id);
    if (!currentUser) {
      throw new Error("User not found");
    }

    // Merge updates with current user
    const mergedUser = { ...currentUser, ...updates };

    const path = `/users/${id}`;
    const payload = {
      name: mergedUser.name,
      email: mergedUser.email,
      type: mapRoleToBackendType(mergedUser.role),
      is_active: mergedUser.isActive,
    };
    const res = await this.client.put(path, { body: payload });
    const body = res.data;
    return mapToAuthUser(body as UserDTO);
  }

  async delete(id: string): Promise<void> {
    const path = `/users/${id}`;
    await this.client.delete(path);
  }

  async updateLastLogin(id: string): Promise<void> {
    // Backend lacks PATCH /users/{id}/last-login endpoint
    // Silently no-op - feature degrades gracefully
    // TODO: Add backend endpoint for last login tracking
    console.warn(`updateLastLogin not implemented in backend for user ${id}`);
  }
}

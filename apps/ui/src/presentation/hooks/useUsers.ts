import { useCallback, useEffect, useState } from "react";

import { AuthUser, UserRole } from "../../domain/entities/User";
import {
  createUserUseCase,
  deleteUserUseCase,
  getUsersByCompanyUseCase,
  searchUsersUseCase,
  updateUserUseCase,
} from "../../infrastructure/di/container";
import { useAuth } from "../contexts/AuthContext";

export function useUsers() {
  const { session } = useAuth();
  const [users, setUsers] = useState<AuthUser[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const loadUsers = useCallback(async () => {
    if (!session) throw new Error("No session");
    try {
      setLoading(true);
      const data = await getUsersByCompanyUseCase.execute(session.company.id, session.user.role);
      setUsers(data);
      setError(null);
    } catch (err) {
      setError(err as Error);
    } finally {
      setLoading(false);
    }
  }, [session]);

  useEffect(() => {
    if (session) {
      loadUsers();
    }
  }, [session, loadUsers]);

  const search = async (query: string, roleFilter?: UserRole) => {
    if (!session) throw new Error("No session");

    try {
      setLoading(true);
      const data = await searchUsersUseCase.execute(session.company.id, query, roleFilter);
      setUsers(data);
      setError(null);
    } catch (err) {
      setError(err as Error);
    } finally {
      setLoading(false);
    }
  };

  const createUser = async (data: {
    name: string;
    email: string;
    password: string;
    role: UserRole;
  }) => {
    if (!session) throw new Error("No session");

    const newUser = await createUserUseCase.execute(
      {
        companyId: session.company.id,
        ...data,
      },
      session.user.role,
    );

    setUsers([...users, newUser]);
    return newUser;
  };

  const updateUser = async (userId: string, updates: Partial<AuthUser>) => {
    if (!session) throw new Error("No session");

    const updatedUser = await updateUserUseCase.execute(userId, updates, session.user.role);

    setUsers(users.map((u) => (u.id === userId ? updatedUser : u)));
    return updatedUser;
  };

  const deleteUser = async (userId: string) => {
    if (!session) throw new Error("No session");

    await deleteUserUseCase.execute(userId, session.user.role);
    setUsers(users.filter((u) => u.id !== userId));
  };

  return {
    users,
    loading,
    error,
    reload: loadUsers,
    search,
    createUser,
    updateUser,
    deleteUser,
  };
}

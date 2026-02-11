import { useCallback, useEffect, useState } from "react";

import { useAuth } from "./useAuth";

import { Customer } from "@/domain/entities/Customer.ts";
import {
  createCustomerUseCase,
  getCustomersByCompanyUseCase,
  searchCustomersUseCase,
} from "@/infrastructure/di/container";

export function useCustomers() {
  const { session } = useAuth();
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const loadCustomers = useCallback(async () => {
    if (!session) throw new Error("No session");

    try {
      setLoading(true);
      const data = await getCustomersByCompanyUseCase.execute(session.company.id);
      setCustomers(data);
      setError(null);
    } catch (err) {
      setError(err as Error);
    } finally {
      setLoading(false);
    }
  }, [session]);

  useEffect(() => {
    if (session) {
      loadCustomers();
    }
  }, [session, loadCustomers]);

  const search = async (query: string) => {
    if (!session) throw new Error("No session");
    try {
      setLoading(true);
      const data = await searchCustomersUseCase.execute(session.company.id, query);
      setCustomers(data);
      setError(null);
    } catch (err) {
      setError(err as Error);
    } finally {
      setLoading(false);
    }
  };

  const createCustomer = async (
    name: string,
    phone: string,
    email: string | null,
    tags: string[],
    notes: string | null,
  ) => {
    if (!session) throw new Error("No session");

    const newCustomer = await createCustomerUseCase.execute(
      session.company.id,
      name,
      phone,
      email,
      tags,
      notes,
    );

    setCustomers([...customers, newCustomer]);
    return newCustomer;
  };

  return { customers, loading, error, reload: loadCustomers, search, createCustomer };
}

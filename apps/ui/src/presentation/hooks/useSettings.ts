import React, { useEffect, useState } from "react";

import { useAuth } from "./useAuth";

import { getCompanyUseCase, updateCompanyUseCase } from "@/infrastructure/di/container.ts";


interface CompanyUpdateFormData {
  name: string;
  email: string;
  phone: string;
  whatsappApiKey: string | null;
  attendantSeesAllConversations: boolean;
}

export function useSettingsState() {
  const { session, hasPermission } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);
  const [error, setError] = useState("");
  const [formData, setFormData] = useState<CompanyUpdateFormData>({
    name: "",
    email: "",
    phone: "",
    whatsappApiKey: "",
    attendantSeesAllConversations: false,
  });

  useEffect(() => {
    if (!session) throw new Error("No session");

    const loadCompany = async () => {
      setIsLoading(true);
      try {
        const company = await getCompanyUseCase.execute(session.company.id, session.user.role);
        setFormData(company);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Erro ao atualizar empresa");
      }
      setIsLoading(false);
    };
    loadCompany();
  }, [session, setFormData]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!session) throw new Error("No session");
    setError("");
    setIsUpdating(true);

    try {
      await updateCompanyUseCase.execute(
        session.company.id,
        formData.name,
        formData.email,
        formData.phone,
        formData.whatsappApiKey,
        formData.attendantSeesAllConversations,
        session.user.role,
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao atualizar empresa");
    } finally {
      setIsUpdating(false);
    }
  };

  return {
    error,
    handleSubmit,
    setFormData,
    formData,
    isLoading,
    isUpdating,
    hasPermission,
  };
}

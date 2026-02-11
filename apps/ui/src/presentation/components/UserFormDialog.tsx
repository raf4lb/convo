import React, { useEffect, useState } from "react";

import { Alert, AlertDescription } from "../../components/ui/alert";
import { Button } from "../../components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "../../components/ui/dialog";
import { Input } from "../../components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../../components/ui/select";

import { AuthUser, User, UserRole } from "@/domain/entities/User.ts";

interface UserDialogProps {
  open: boolean;
  setOpen: (open: boolean) => void;
  onSubmit: (data: Partial<User>) => Promise<void>;
  user?: AuthUser; // se vier preenchido, estamos editando
  canCreateAttendant?: boolean;
  canCreateManager?: boolean;
  canCreateAdmin?: boolean;
}

export function UserFormDialog({
  open,
  setOpen,
  onSubmit,
  user,
  canCreateAttendant,
  canCreateManager,
  canCreateAdmin,
}: UserDialogProps) {
  const isEdit = !!user;

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    role: UserRole.ATTENDANT,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isEdit && user) {
      setFormData({
        name: user.name,
        email: user.email,
        password: "",
        role: user.role,
      });
    } else {
      setFormData({
        name: "",
        email: "",
        password: "",
        role: UserRole.ATTENDANT,
      });
    }
  }, [user, isEdit, open]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await onSubmit(formData);
      setOpen(false);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Erro ao salvar usuário");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Dialog
      open={open}
      onOpenChange={() => {
        setOpen(false);
        setError(null);
      }}
    >
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{isEdit ? "Editar Usuário" : "Criar Novo Usuário"}</DialogTitle>
          <DialogDescription>
            {isEdit ? "Atualize as informações do usuário." : "Adicione um novo usuário à empresa."}
          </DialogDescription>
        </DialogHeader>

        {error && (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <form onSubmit={handleSubmit} className="space-y-4 mt-4">
          <Input
            placeholder="Nome completo"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
            disabled={loading}
          />

          <Input
            type="email"
            placeholder="email@empresa.com"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            required
            disabled={loading}
          />

          {!isEdit && (
            <Input
              type="password"
              placeholder="Senha (mínimo 6 caracteres)"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              required
              disabled={loading}
            />
          )}

          <Select
            value={formData.role}
            onValueChange={(value: UserRole) => setFormData({ ...formData, role: value })}
            disabled={loading}
          >
            <SelectTrigger>
              <SelectValue placeholder="Selecione o tipo de usuário" />
            </SelectTrigger>
            <SelectContent>
              {canCreateAttendant && <SelectItem value={UserRole.ATTENDANT}>Atendente</SelectItem>}
              {canCreateManager && <SelectItem value={UserRole.MANAGER}>Gerente</SelectItem>}
              {canCreateAdmin && (
                <SelectItem value={UserRole.ADMINISTRATOR}>Administrador</SelectItem>
              )}
            </SelectContent>
          </Select>

          <Button
            type="submit"
            className="w-full bg-green-500 hover:bg-green-600"
            disabled={loading}
          >
            {loading ? (isEdit ? "Salvando..." : "Criando...") : isEdit ? "Salvar" : "Criar"}
          </Button>
        </form>
      </DialogContent>
    </Dialog>
  );
}

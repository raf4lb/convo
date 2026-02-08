import React, { useState } from "react";

import { Mail, MoreVertical, Phone, Plus, Search, Tag } from "lucide-react";

import { Alert, AlertDescription } from "../../components/ui/alert";
import { Badge } from "../../components/ui/badge";
import { Button } from "../../components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../../components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "../../components/ui/dialog";
import { Input } from "../../components/ui/input";
import { Textarea } from "../../components/ui/textarea";
import { useAuth } from "../contexts/AuthContext";
import { useCustomers } from "../hooks/useCustomers";

export function CustomerManagement() {
  const { session } = useAuth();
  const { customers, loading, search, createCustomer } = useCustomers();
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [formData, setFormData] = useState({
    name: "",
    phone: "",
    email: "",
    tags: "",
    notes: "",
  });
  const [error, setError] = useState("");
  const [creating, setCreating] = useState(false);

  if (!session) return null;

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    search(query);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setCreating(true);

    try {
      const tags = formData.tags
        .split(",")
        .map((t) => t.trim())
        .filter((t) => t.length > 0);

      await createCustomer(
        formData.name,
        formData.phone,
        formData.email || null,
        tags.length > 0 ? tags : [],
        formData.notes || null,
      );

      setIsDialogOpen(false);
      setFormData({
        name: "",
        phone: "",
        email: "",
        tags: "",
        notes: "",
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao criar cliente");
    } finally {
      setCreating(false);
    }
  };

  const formatDate = (date?: Date) => {
    if (!date) return "Nunca";
    return new Date(date).toLocaleDateString("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <div className="flex-1 flex flex-col bg-white">
      {/* Header */}
      <div className="border-b border-neutral-200 p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="mb-1">Clientes</h2>
            <p className="text-sm text-neutral-500">
              Gerencie os clientes da empresa {session.company.name}
            </p>
          </div>
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button className="bg-green-500 hover:bg-green-600 gap-2">
                <Plus className="w-4 h-4" />
                Novo Cliente
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Adicionar Novo Cliente</DialogTitle>
                <DialogDescription>Cadastre um novo cliente na sua base</DialogDescription>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="space-y-4">
                {error && (
                  <Alert variant="destructive">
                    <AlertDescription>{error}</AlertDescription>
                  </Alert>
                )}

                <div className="space-y-2">
                  <label htmlFor="customer-name" className="text-sm text-neutral-700">
                    Nome *
                  </label>
                  <Input
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    placeholder="Nome do cliente"
                    required
                    disabled={creating}
                  />
                </div>

                <div className="space-y-2">
                  <label htmlFor="customer-phone" className="text-sm text-neutral-700">
                    Telefone *
                  </label>
                  <Input
                    value={formData.phone}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    placeholder="+55 11 98765-4321"
                    required
                    disabled={creating}
                  />
                </div>

                <div className="space-y-2">
                  <label htmlFor="customer-email" className="text-sm text-neutral-700">
                    Email
                  </label>
                  <Input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    placeholder="email@exemplo.com"
                    disabled={creating}
                  />
                </div>

                <div className="space-y-2">
                  <label htmlFor="customer-tags" className="text-sm text-neutral-700">
                    Tags
                  </label>
                  <Input
                    value={formData.tags}
                    onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
                    placeholder="VIP, Cliente Recorrente (separado por vírgula)"
                    disabled={creating}
                  />
                </div>

                <div className="space-y-2">
                  <label htmlFor="customer-notes" className="text-sm text-neutral-700">
                    Observações
                  </label>
                  <Textarea
                    value={formData.notes}
                    onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                    placeholder="Informações adicionais sobre o cliente"
                    disabled={creating}
                    rows={3}
                  />
                </div>

                <Button
                  type="submit"
                  className="w-full bg-green-500 hover:bg-green-600"
                  disabled={creating}
                >
                  {creating ? "Cadastrando..." : "Cadastrar Cliente"}
                </Button>
              </form>
            </DialogContent>
          </Dialog>
        </div>

        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-neutral-400" />
          <Input
            placeholder="Buscar por nome, telefone, email ou tags..."
            className="pl-9 bg-neutral-50 border-0"
            value={searchQuery}
            onChange={(e) => handleSearch(e.target.value)}
          />
        </div>
      </div>

      {/* Customers List */}
      <div className="flex-1 overflow-y-auto p-6">
        {loading ? (
          <p className="text-neutral-500 text-center">Carregando...</p>
        ) : customers.length === 0 ? (
          <p className="text-neutral-500 text-center">Nenhum cliente encontrado</p>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
            {customers.map((customer) => (
              <Card key={customer.id}>
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-12 h-12 rounded-full bg-linear-to-br from-green-400 to-green-600 flex items-center justify-center text-white">
                        {customer.name
                          .split(" ")
                          .map((n) => n[0])
                          .join("")
                          .substring(0, 2)}
                      </div>
                      <div className="flex-1 min-w-0">
                        <CardTitle className="text-base truncate">{customer.name}</CardTitle>
                        <p className="text-xs text-neutral-500 flex items-center gap-1 mt-0.5">
                          <Phone className="w-3 h-3" />
                          {customer.phone}
                        </p>
                        {customer.email && (
                          <p className="text-xs text-neutral-500 flex items-center gap-1">
                            <Mail className="w-3 h-3" />
                            {customer.email}
                          </p>
                        )}
                      </div>
                    </div>
                    <Button variant="ghost" size="icon" className="h-8 w-8">
                      <MoreVertical className="w-4 h-4" />
                    </Button>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  {customer.tags && customer.tags.length > 0 && (
                    <div className="flex flex-wrap gap-1">
                      {customer.tags.map((tag, index) => (
                        <Badge key={index} variant="outline" className="text-xs bg-neutral-50">
                          <Tag className="w-3 h-3 mr-1" />
                          {tag}
                        </Badge>
                      ))}
                    </div>
                  )}

                  {customer.notes && (
                    <p className="text-sm text-neutral-600 line-clamp-2">{customer.notes}</p>
                  )}

                  <div className="pt-2 border-t border-neutral-100">
                    <p className="text-xs text-neutral-500">
                      Último contato:{" "}
                      {customer.lastContactAt ? formatDate(customer.lastContactAt) : "-"}
                    </p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

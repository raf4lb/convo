import { useState } from "react";

import { Edit, MoreVertical, Plus, Search, Trash2 } from "lucide-react";

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "../../components/ui/alert-dialog";
import { Badge } from "../../components/ui/badge";
import { Button } from "../../components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../../components/ui/card";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "../../components/ui/dropdown-menu";
import { Input } from "../../components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../../components/ui/select";
import { Permission } from "../../domain/entities/Permission";
import { AuthUser, User, UserRole } from "../../domain/entities/User";
import { useAuth } from "../contexts/AuthContext";
import { useUsers } from "../hooks/useUsers";

import { RoleBadge } from "./RoleBadge";
import { UserFormDialog } from "./UserFormDialog";

export function UserManagement() {
  const { session, hasPermission } = useAuth();
  const { users, loading, search, createUser, updateUser, deleteUser } = useUsers();
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState<AuthUser | null>(null);
  const [deleteUserId, setDeleteUserId] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [roleFilter, setRoleFilter] = useState<UserRole | "all">("all");
  const [deleting, setDeleting] = useState(false);

  if (!session) return null;

  const canCreateAdmin = hasPermission(Permission.CREATE_ADMINISTRATOR);
  const canCreateManager = hasPermission(Permission.CREATE_MANAGER);
  const canCreateAttendant = hasPermission(Permission.CREATE_ATTENDANT);
  const canCreateAny = canCreateAdmin || canCreateManager || canCreateAttendant;

  const handleSearch = (query: string, role?: UserRole | "all") => {
    setSearchQuery(query);
    const roleToSearch = role !== "all" ? role : undefined;
    search(query, roleToSearch);
  };

  const handleRoleFilterChange = (role: string) => {
    const selectedRole = role as UserRole | "all";
    setRoleFilter(selectedRole);
    handleSearch(searchQuery, selectedRole);
  };

  const handleCreate = async (data: Partial<User>) => {
    await createUser({
      name: data.name || "",
      email: data.email || "",
      password: data.password || "",
      role: data.role || UserRole.ATTENDANT,
    });
  };

  const handleUpdate = async (data: Partial<User>) => {
    if (!selectedUser) return;
    await updateUser(selectedUser.id, {
      name: data.name || "",
      email: data.email || "",
      role: data.role || UserRole.ATTENDANT,
    });
  };

  const handleDelete = async () => {
    if (!deleteUserId) return;

    setDeleting(true);
    try {
      await deleteUser(deleteUserId);
      setDeleteUserId(null);
    } catch (err) {
      console.error("Error deleting user:", err);
    } finally {
      setDeleting(false);
    }
  };

  const canEditUser = (userRole: UserRole) => {
    if (userRole === UserRole.ADMINISTRATOR) return canCreateAdmin;
    if (userRole === UserRole.MANAGER) return canCreateManager;
    if (userRole === UserRole.ATTENDANT) return canCreateAttendant;
    return false;
  };

  return (
    <div className="flex-1 flex flex-col bg-white">
      {/* Header */}
      <div className="border-b border-neutral-200 p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="mb-1">Usuários</h2>
            <p className="text-sm text-neutral-500">
              Gerencie os usuários da empresa {session.company.name}
            </p>
          </div>
          {canCreateAny && (
            <div>
              <Button
                onClick={() => {
                  setSelectedUser(null);
                  setIsCreateDialogOpen(true);
                }}
                className="bg-green-500 hover:bg-green-600 gap-2"
              >
                <Plus className="w-4 h-4" />
                Novo Usuário
              </Button>
              <UserFormDialog
                open={isCreateDialogOpen}
                setOpen={setIsCreateDialogOpen}
                onSubmit={handleCreate}
                canCreateAdmin={canCreateAdmin}
                canCreateManager={canCreateManager}
                canCreateAttendant={canCreateAttendant}
              />
            </div>
          )}
        </div>

        {/* Search and Filters */}
        <div className="flex gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-neutral-400" />
            <Input
              placeholder="Buscar por nome ou email..."
              className="pl-9 bg-neutral-50 border-0"
              value={searchQuery}
              onChange={(e) => handleSearch(e.target.value, roleFilter)}
            />
          </div>
          <Select value={roleFilter} onValueChange={handleRoleFilterChange}>
            <SelectTrigger className="w-48 bg-neutral-50 border-0">
              <SelectValue placeholder="Filtrar por tipo" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todos os tipos</SelectItem>
              {canCreateAttendant && <SelectItem value={UserRole.ATTENDANT}>Atendentes</SelectItem>}
              {canCreateManager && <SelectItem value={UserRole.MANAGER}>Gerentes</SelectItem>}
              {canCreateAdmin && (
                <SelectItem value={UserRole.ADMINISTRATOR}>Administradores</SelectItem>
              )}
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Users List */}
      <div className="flex-1 overflow-y-auto p-6">
        {loading ? (
          <p className="text-neutral-500 text-center">Carregando...</p>
        ) : users.length === 0 ? (
          <p className="text-neutral-500 text-center">Nenhum usuário encontrado</p>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
            {users.map((user) => (
              <Card key={user.id}>
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-12 h-12 rounded-full bg-linear-to-br from-green-400 to-green-600 flex items-center justify-center text-white">
                        {user.name
                          .split(" ")
                          .map((n) => n[0])
                          .join("")
                          .substring(0, 2)}
                      </div>
                      <div>
                        <CardTitle
                          onClick={() => {
                            setSelectedUser(user);
                            setIsEditDialogOpen(true);
                          }}
                          className="text-base"
                        >
                          {user.name}
                        </CardTitle>
                        <p className="text-xs text-neutral-500 mt-0.5">{user.email}</p>
                      </div>
                    </div>
                    {canEditUser(user.role) && (
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" size="icon" className="h-8 w-8">
                            <MoreVertical className="w-4 h-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuItem
                            onClick={() => {
                              setSelectedUser(user);
                              setIsEditDialogOpen(true);
                            }}
                          >
                            <Edit className="w-4 h-4 mr-2" />
                            Editar
                          </DropdownMenuItem>
                          <DropdownMenuItem
                            className="text-red-600"
                            onClick={() => setDeleteUserId(user.id)}
                          >
                            <Trash2 className="w-4 h-4 mr-2" />
                            Deletar
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    )}
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between">
                    <RoleBadge role={user.role} />
                    <Badge
                      variant={user.isActive ? "default" : "secondary"}
                      className={user.isActive ? "bg-green-50 text-green-700 border-green-200" : ""}
                    >
                      {user.isActive ? "Ativo" : "Inativo"}
                    </Badge>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>

      {/* Edit Dialog */}
      {selectedUser && (
        <UserFormDialog
          open={isEditDialogOpen}
          setOpen={(open) => {
            setIsEditDialogOpen(open);
            if (!open) setSelectedUser(null);
          }}
          onSubmit={handleUpdate}
          user={selectedUser}
          canCreateAdmin={canCreateAdmin}
          canCreateManager={canCreateManager}
          canCreateAttendant={canCreateAttendant}
        />
      )}

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={!!deleteUserId} onOpenChange={() => setDeleteUserId(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Confirmar exclusão</AlertDialogTitle>
            <AlertDialogDescription>
              Tem certeza que deseja deletar este usuário? Esta ação não pode ser desfeita.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel disabled={deleting}>Cancelar</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleDelete}
              disabled={deleting}
              className="bg-red-600 hover:bg-red-700"
            >
              {deleting ? "Deletando..." : "Deletar"}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}

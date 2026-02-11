import { BarChart3, LogOut, MessageSquare, Settings, User, Users } from "lucide-react";

import { Avatar, AvatarFallback } from "../../components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "../../components/ui/dropdown-menu";
import { View } from "../constants/views";
import { useAuth } from "../hooks/useAuth";

import { Login } from "./Login";

import { Permission } from "@/domain/entities/Permission.ts";

interface SidebarProps {
  selectedView: View;
  onViewChange: (view: View) => void;
}

export function Sidebar({ selectedView, onViewChange }: SidebarProps) {
  const { session, logout, hasPermission } = useAuth();

  if (!session) return <Login />;

  const menuItems = [
    {
      id: View.DASHBOARD,
      icon: BarChart3,
      label: "Dashboard",
      permission: Permission.VIEW_DASHBOARD,
    },
    {
      id: View.CONVERSATIONS,
      icon: MessageSquare,
      label: "Conversas",
      permission: Permission.VIEW_CONVERSATIONS,
    },
    {
      id: View.CUSTOMERS,
      icon: Users,
      label: "Clientes",
      permission: Permission.VIEW_CUSTOMERS,
    },
  ].filter((item) => hasPermission(item.permission));

  return (
    <div className="w-16 bg-white border-r border-neutral-200 flex flex-col items-center py-6 gap-6">
      {/* Logo */}
      <div className="w-10 h-10 bg-green-500 rounded-xl flex items-center justify-center">
        <MessageSquare className="w-6 h-6 text-white" />
      </div>

      {/* Menu Items */}
      <nav className="flex flex-col gap-2">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isSelected = selectedView === item.id;

          return (
            <button
              key={item.id}
              onClick={() => onViewChange(item.id)}
              className={`w-11 h-11 rounded-xl flex items-center justify-center transition-colors ${
                isSelected
                  ? "bg-green-50 text-green-600"
                  : "text-neutral-400 hover:bg-neutral-50 hover:text-neutral-600"
              }`}
              title={item.label}
            >
              <Icon className="w-5 h-5" />
            </button>
          );
        })}
      </nav>

      {/* User Menu at bottom */}
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <button className="mt-auto w-11 h-11 rounded-xl flex items-center justify-center hover:bg-neutral-50 transition-colors">
            <Avatar className="w-10 h-10">
              <AvatarFallback className="bg-gradient-to-br from-green-400 to-green-600 text-white text-sm">
                {session.user.name
                  .split(" ")
                  .map((n) => n[0])
                  .join("")
                  .substring(0, 2)}
              </AvatarFallback>
            </Avatar>
          </button>
        </DropdownMenuTrigger>
        <DropdownMenuContent side="right" align="end" className="w-56">
          <DropdownMenuLabel>
            <div className="flex flex-col">
              <span className="text-sm">{session.user.name}</span>
              <span className="text-xs text-neutral-500">{session.user.email}</span>
            </div>
          </DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuItem onClick={() => onViewChange(View.PROFILE)}>
            <User className="w-4 h-4 mr-2" />
            Minha Conta
          </DropdownMenuItem>
          <DropdownMenuSeparator />
          {hasPermission(Permission.VIEW_SETTINGS) && (
            <div>
              <DropdownMenuItem onClick={() => onViewChange(View.SETTINGS)}>
                <Settings className="w-4 h-4 mr-2" />
                Configurações
              </DropdownMenuItem>
              <DropdownMenuSeparator />
            </div>
          )}
          <DropdownMenuItem onClick={() => onViewChange(View.USERS)}>
            <Users className="w-4 h-4 mr-2" />
            Usuários
          </DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem onClick={logout} className="text-red-600">
            <LogOut className="w-4 h-4 mr-2" />
            Sair
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}

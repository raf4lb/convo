import { AlertCircle } from "lucide-react";

import { Alert, AlertDescription } from "../../components/ui/alert";
import { Button } from "../../components/ui/button";
import { Card, CardContent } from "../../components/ui/card";
import { Input } from "../../components/ui/input";
import { Switch } from "../../components/ui/switch";
import { Permission } from "../../domain/entities/Permission";
import { useSettingsState } from "../hooks/useSettings";

import { Dashboard } from "./Dashboard";

export function Settings() {
  const settingsState = useSettingsState();

  if (!settingsState.hasPermission(Permission.VIEW_SETTINGS)) {
    return <Dashboard />;
  }

  return (
    <div className="flex-1 flex flex-col bg-white">
      {/* Header */}
      <div className="border-b border-neutral-200 p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="mb-1">Configurações</h2>
            <p className="text-sm text-neutral-500">Gerencie as configurações da empresa</p>
          </div>
        </div>
      </div>

      <div className="overflow-y-auto p-6">
        <div className="grid lg:grid-cols-2 md:grid-cols-1 sm:grid-cols-1 xs:grid-cols-1">
          <Card className="bg-white border-b border-neutral-200">
            <CardContent className="mt-6">
              {settingsState.error && (
                <Alert variant="destructive" className="mb-4 bg-red-50 text-red-700 border-red-200">
                  <AlertCircle />
                  <AlertDescription>{settingsState.error}</AlertDescription>
                </Alert>
              )}
              <form onSubmit={settingsState.handleSubmit} className="space-y-5">
                <div className="w-full">
                  <label htmlFor="company-name" className="text-sm text-neutral-700">
                    Nome
                  </label>
                  <Input
                    id="company-name"
                    className="mt-1"
                    placeholder="Nome da Empresa"
                    value={settingsState.formData.name}
                    onChange={(e) =>
                      settingsState.setFormData({ ...settingsState.formData, name: e.target.value })
                    }
                    required
                    disabled={settingsState.isLoading}
                  />
                </div>

                <div className="">
                  <label htmlFor="company-email" className="text-sm text-neutral-700">
                    Email
                  </label>
                  <Input
                    className="mt-1"
                    id="company-email"
                    placeholder="email@empresa.com"
                    value={settingsState.formData.email}
                    onChange={(e) =>
                      settingsState.setFormData({
                        ...settingsState.formData,
                        email: e.target.value,
                      })
                    }
                    required
                    disabled={settingsState.isLoading}
                  />
                </div>

                <div>
                  <label htmlFor="company-phone" className="text-sm text-neutral-700">
                    Telefone
                  </label>
                  <Input
                    className="mt-1"
                    id="company-phone"
                    placeholder="(88) 99999-9999"
                    value={settingsState.formData.phone}
                    onChange={(e) =>
                      settingsState.setFormData({
                        ...settingsState.formData,
                        phone: e.target.value,
                      })
                    }
                    required
                    disabled={settingsState.isLoading}
                  />
                </div>

                <div>
                  <label htmlFor="company-whatsapp-api-key" className="text-sm text-neutral-700">
                    API Key
                  </label>
                  <Input
                    className="mt-1"
                    id="company-whatsapp-api-key"
                    placeholder="whatsapp-api-key"
                    value={settingsState.formData.whatsappApiKey}
                    onChange={(e) =>
                      settingsState.setFormData({
                        ...settingsState.formData,
                        whatsappApiKey: e.target.value,
                      })
                    }
                    required
                    disabled={settingsState.isLoading}
                  />
                </div>

                <div>
                  <p className="text-sm text-neutral-700">Atendentes veem todas as conversas</p>
                  <div className="flex items-center justify-between w-full py-1 mt-1">
                    <label
                      htmlFor="attendant-sees-all-conversations"
                      className="text-sm text-muted-foreground"
                    >
                      Se desativado, atendentes verão apenas as suas conversas
                    </label>
                    <Switch
                      id="attendant-sees-all-conversations"
                      checked={settingsState.formData.attendantSeesAllConversations}
                      onCheckedChange={(value: boolean) =>
                        settingsState.setFormData({
                          ...settingsState.formData,
                          attendantSeesAllConversations: value,
                        })
                      }
                      className="data-[state=checked]:bg-green-500 ml-4"
                      disabled={settingsState.isLoading}
                    />
                  </div>
                </div>
                <Button type="submit" variant="default" disabled={settingsState.isLoading}>
                  {settingsState.isLoading || settingsState.isUpdating
                    ? settingsState.isUpdating
                      ? "Salvando..."
                      : "Carregando..."
                    : "Salvar"}
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

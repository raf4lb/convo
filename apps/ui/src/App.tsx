import { useState } from "react";

import { Chat } from "./presentation/components/Chat";
import { CustomerManagement } from "./presentation/components/CustomerManagement";
import { Dashboard } from "./presentation/components/Dashboard";
import { Login } from "./presentation/components/Login";
import { Settings } from "./presentation/components/Settings";
import { Sidebar } from "./presentation/components/Sidebar";
import { UserManagement } from "./presentation/components/UserManagement";
import { View } from "./presentation/constants/views";
import { AuthProvider } from "./presentation/contexts/AuthContext";
import { useAuth } from "./presentation/hooks/useAuth";

function AppContent() {
  const { session, loading } = useAuth();
  const [selectedView, setSelectedView] = useState<View>(View.DASHBOARD);

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-neutral-50">
        <p className="text-neutral-500">Carregando...</p>
      </div>
    );
  }

  if (!session) {
    return <Login />;
  }

  return (
    <div className="flex h-screen bg-neutral-50">
      {/* Sidebar */}
      <Sidebar selectedView={selectedView} onViewChange={setSelectedView} />

      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        {selectedView === View.DASHBOARD ? (
          <Dashboard />
        ) : selectedView === View.CUSTOMERS ? (
          <CustomerManagement />
        ) : selectedView === View.USERS ? (
          <UserManagement />
        ) : selectedView === View.SETTINGS ? (
          <Settings />
        ) : (
          <Chat />
        )}
      </div>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

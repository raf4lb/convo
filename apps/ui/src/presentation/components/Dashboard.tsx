import { Calendar, Clock, MessageSquare, ThumbsUp, TrendingUp, Users } from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { Card, CardContent, CardHeader, CardTitle } from "../../components/ui/card";
import { useMetrics } from "../hooks/useMetrics";

export function Dashboard() {
  const {
    metrics,
    conversationsByDay,
    attendantPerformance,
    hourlyData,
    statusData,
    detailedPerformance,
    loading,
  } = useMetrics();

  if (loading || !metrics) {
    return (
      <div className="flex-1 flex items-center justify-center bg-neutral-50">
        <p className="text-neutral-500">Carregando métricas...</p>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto bg-neutral-50">
      <div className="p-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <h1>Dashboard de Atendimento</h1>
            <div className="flex items-center gap-2 text-sm text-neutral-500">
              <Calendar className="w-4 h-4" />
              Últimos 7 dias
            </div>
          </div>
          <p className="text-neutral-600">Acompanhe métricas e performance da sua equipe</p>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm text-neutral-600">Total de Conversas</CardTitle>
              <MessageSquare className="w-4 h-4 text-green-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl text-neutral-900 mb-1">{metrics.totalConversations}</div>
              <p className="text-xs text-green-600 flex items-center gap-1">
                <TrendingUp className="w-3 h-3" />+{metrics.trend.conversations}% vs semana anterior
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm text-neutral-600">Tempo Médio de Resposta</CardTitle>
              <Clock className="w-4 h-4 text-blue-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl text-neutral-900 mb-1">{metrics.averageResponseTime}</div>
              <p className="text-xs text-green-600 flex items-center gap-1">
                <TrendingUp className="w-3 h-3" />
                {metrics.trend.responseTime}% mais rápido
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm text-neutral-600">Taxa de Satisfação</CardTitle>
              <ThumbsUp className="w-4 h-4 text-amber-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl text-neutral-900 mb-1">{metrics.satisfactionRate}/5.0</div>
              <p className="text-xs text-green-600 flex items-center gap-1">
                <TrendingUp className="w-3 h-3" />+{metrics.trend.satisfaction} pontos
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm text-neutral-600">Atendentes Ativos</CardTitle>
              <Users className="w-4 h-4 text-purple-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl text-neutral-900 mb-1">
                {metrics.activeAttendants}/{metrics.totalAttendants}
              </div>
              <p className="text-xs text-neutral-500">
                {metrics.activeConversationsCount} conversas ativas
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Charts Row 1 */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          {/* Conversas por Dia */}
          <Card className="lg:col-span-2">
            <CardHeader>
              <CardTitle>Conversas por Dia</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={conversationsByDay}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e5e5" />
                  <XAxis dataKey="date" stroke="#737373" style={{ fontSize: "12px" }} />
                  <YAxis stroke="#737373" style={{ fontSize: "12px" }} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "white",
                      border: "1px solid #e5e5e5",
                      borderRadius: "8px",
                      fontSize: "14px",
                    }}
                  />
                  <Legend wrapperStyle={{ fontSize: "14px" }} iconType="circle" />
                  <Line
                    type="monotone"
                    dataKey="conversas"
                    stroke="#00a63e"
                    strokeWidth={2}
                    name="Total"
                    dot={{ fill: "#00a63e", r: 4 }}
                  />
                  <Line
                    type="monotone"
                    dataKey="resolvidas"
                    stroke="#3b82f6"
                    strokeWidth={2}
                    name="Resolvidas"
                    dot={{ fill: "#3b82f6", r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Status das Conversas */}
          <Card>
            <CardHeader>
              <CardTitle>Status das Conversas</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={statusData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {statusData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "white",
                      border: "1px solid #e5e5e5",
                      borderRadius: "8px",
                      fontSize: "14px",
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* Charts Row 2 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Performance por Atendente */}
          <Card>
            <CardHeader>
              <CardTitle>Conversas por Atendente</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={attendantPerformance}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e5e5" />
                  <XAxis dataKey="name" stroke="#737373" style={{ fontSize: "12px" }} />
                  <YAxis stroke="#737373" style={{ fontSize: "12px" }} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "white",
                      border: "1px solid #e5e5e5",
                      borderRadius: "8px",
                      fontSize: "14px",
                    }}
                  />
                  <Bar dataKey="conversas" fill="#00a63e" radius={[8, 8, 0, 0]} name="Conversas" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Mensagens por Horário */}
          <Card>
            <CardHeader>
              <CardTitle>Volume por Horário</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={hourlyData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e5e5" />
                  <XAxis dataKey="hora" stroke="#737373" style={{ fontSize: "12px" }} />
                  <YAxis stroke="#737373" style={{ fontSize: "12px" }} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "white",
                      border: "1px solid #e5e5e5",
                      borderRadius: "8px",
                      fontSize: "14px",
                    }}
                  />
                  <Bar dataKey="mensagens" fill="#3b82f6" radius={[8, 8, 0, 0]} name="Mensagens" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* Performance Table */}
        <Card>
          <CardHeader>
            <CardTitle>Performance Detalhada dos Atendentes</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-neutral-200">
                    <th className="text-left py-3 px-4 text-sm text-neutral-600">Atendente</th>
                    <th className="text-left py-3 px-4 text-sm text-neutral-600">
                      Conversas Totais
                    </th>
                    <th className="text-left py-3 px-4 text-sm text-neutral-600">Ativas</th>
                    <th className="text-left py-3 px-4 text-sm text-neutral-600">Resolvidas</th>
                    <th className="text-left py-3 px-4 text-sm text-neutral-600">Tempo Médio</th>
                    <th className="text-left py-3 px-4 text-sm text-neutral-600">Satisfação</th>
                  </tr>
                </thead>
                <tbody>
                  {detailedPerformance.map((attendant) => (
                    <tr
                      key={attendant.name}
                      className="border-b border-neutral-100 hover:bg-neutral-50"
                    >
                      <td className="py-3 px-4">
                        <div className="flex items-center gap-3">
                          <div className="w-8 h-8 rounded-full bg-linear-to-br from-green-400 to-green-600 flex items-center justify-center text-white text-sm">
                            {attendant.name.charAt(0)}
                          </div>
                          <span className="text-neutral-900">{attendant.name}</span>
                        </div>
                      </td>
                      <td className="py-3 px-4 text-neutral-700">{attendant.total}</td>
                      <td className="py-3 px-4">
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-blue-50 text-blue-700">
                          {attendant.active}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-green-50 text-green-700">
                          {attendant.resolved}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-neutral-700">{attendant.avgTime}</td>
                      <td className="py-3 px-4">
                        <div className="flex items-center gap-1">
                          <ThumbsUp className="w-4 h-4 text-amber-500" />
                          <span className="text-neutral-900">{attendant.satisfaction}</span>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

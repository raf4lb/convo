// Dependency Injection Container

import { InMemoryEventBus } from "../events/EventBus";
import { AuthInterceptor } from "../http/AuthInterceptor";
import { HttpClient } from "../http/HttpClient";
import { WebSocketAdapter } from "../websocket/WebSocketAdapter";
import { onMessageReceivedHandler } from "../websocket/WebSocketHandlers";

import { ApiAuthRepository } from "@/data/repositories/ApiAuthRepository.ts";
import { ApiCompanyRepository } from "@/data/repositories/ApiCompanyRepository";
import { ApiConversationRepository } from "@/data/repositories/ApiConversationRepository";
import { ApiCustomerRepository } from "@/data/repositories/ApiCustomerRepository";
import { ApiUserRepository } from "@/data/repositories/ApiUserRepository";
import { MockAttendantStatsRepository } from "@/data/repositories/MockAttendantStatsRepository";
import { MockMetricsRepository } from "@/data/repositories/MockMetricsRepository";
import { Login } from "@/domain/use-cases/auth/Login";
import { Logout } from "@/domain/use-cases/auth/Logout";
import { ValidateSession } from "@/domain/use-cases/auth/ValidateSession";
import { GetCompany } from "@/domain/use-cases/company/GetCompany";
import { UpdateCompany } from "@/domain/use-cases/company/UpdateCompany";
import { AssignConversationToAttendant } from "@/domain/use-cases/conversation/AssignConversationToAttendant";
import { GetConversation } from "@/domain/use-cases/conversation/GetConversation";
import { GetConversationMessages } from "@/domain/use-cases/conversation/GetConversationMessages";
import { GetConversations } from "@/domain/use-cases/conversation/GetConversations";
import { MarkConversationAsRead } from "@/domain/use-cases/conversation/MarkConversationAsRead";
import { ReceiveMessage } from "@/domain/use-cases/conversation/ReceiveMessage";
import { SearchConversations } from "@/domain/use-cases/conversation/SearchConversations";
import { SendMessage } from "@/domain/use-cases/conversation/SendMessage";
import { CreateCustomer } from "@/domain/use-cases/customer/CreateCustomer";
import { GetCustomersByCompany } from "@/domain/use-cases/customer/GetCustomersByCompany";
import { SearchCustomers } from "@/domain/use-cases/customer/SearchCustomers";
import { GetDashboardMetrics } from "@/domain/use-cases/GetDashboardMetrics";
import { CheckPermission } from "@/domain/use-cases/user/CheckPermission";
import { CreateUser } from "@/domain/use-cases/user/CreateUser";
import { DeleteUser } from "@/domain/use-cases/user/DeleteUser";
import { GetUsersByCompany } from "@/domain/use-cases/user/GetUsersByCompany";
import { SearchUsers } from "@/domain/use-cases/user/SearchUsers";
import { UpdateUser } from "@/domain/use-cases/user/UpdateUser";

// WebSockets
const WS_MESSAGES_URL = import.meta.env.VITE_WS_URL || "ws://localhost:8000/ws";
export const messagesWebSocket = new WebSocketAdapter(
  WS_MESSAGES_URL,
  30, // maxReconnectAttempts
  1000, // baseBackoffMs (1 second)
);
messagesWebSocket.addHandler(onMessageReceivedHandler);

// EventBus
export const eventBus = new InMemoryEventBus();

// HTTP Client with Auth Interceptor
const baseUrl = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
const client = new HttpClient(baseUrl, 30000, 3);
const authInterceptor = new AuthInterceptor(baseUrl);
client.addResponseInterceptor(authInterceptor.createResponseInterceptor());

// Repositories (Singleton instances)
const conversationRepository = new ApiConversationRepository(client);
const metricsRepository = new MockMetricsRepository();
const companyRepository = new ApiCompanyRepository(client);
const userRepository = new ApiUserRepository(client);
const authRepository = new ApiAuthRepository(client, companyRepository);
const customerRepository = new ApiCustomerRepository(client);
const attendantStatsRepository = new MockAttendantStatsRepository();

// Company Use Cases
export const updateCompanyUseCase = new UpdateCompany(companyRepository);
export const getCompanyUseCase = new GetCompany(companyRepository);

// Conversation Use Cases
export const getConversationUseCase = new GetConversation(
  conversationRepository,
  companyRepository,
);
export const getConversationsUseCase = new GetConversations(
  conversationRepository,
  companyRepository,
);
export const getConversationMessagesUseCase = new GetConversationMessages(conversationRepository);
export const assignConversationToAttendantUseCase = new AssignConversationToAttendant(
  conversationRepository,
  eventBus,
);
export const sendMessageUseCase = new SendMessage(conversationRepository, eventBus);
export const receiveMessageUseCase = new ReceiveMessage(conversationRepository, eventBus);
export const searchConversationsUseCase = new SearchConversations(conversationRepository);
export const markConversationAsReadUseCase = new MarkConversationAsRead(
  conversationRepository,
  eventBus,
);

// Metrics Use Cases
export const getDashboardMetricsUseCase = new GetDashboardMetrics(metricsRepository);

// Auth Use Cases
export const loginUseCase = new Login(authRepository, messagesWebSocket);
export const logoutUseCase = new Logout(authRepository, messagesWebSocket);
export const validateSessionUseCase = new ValidateSession(authRepository);

// User Use Cases
export const createUserUseCase = new CreateUser(userRepository);
export const getUsersByCompanyUseCase = new GetUsersByCompany(userRepository);
export const updateUserUseCase = new UpdateUser(userRepository);
export const deleteUserUseCase = new DeleteUser(userRepository);
export const searchUsersUseCase = new SearchUsers(userRepository);
export const checkPermissionUseCase = new CheckPermission();

// Customer Use Cases
export const getCustomersByCompanyUseCase = new GetCustomersByCompany(customerRepository);
export const searchCustomersUseCase = new SearchCustomers(customerRepository);
export const createCustomerUseCase = new CreateCustomer(customerRepository);

// Repositories (direct access for complex queries)
export { attendantStatsRepository, conversationRepository, metricsRepository };

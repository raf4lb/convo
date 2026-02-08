// Dependency Injection Container

import { ApiCompanyRepository } from "../../data/repositories/ApiCompanyRepository";
import { ApiCustomerRepository } from "../../data/repositories/ApiCustomerRepository";
import { AttendantStatsRepository } from "../../data/repositories/AttendantStatsRepository";
import { AuthRepository } from "../../data/repositories/AuthRepository";
import { ConversationRepository } from "../../data/repositories/ConversationRepository";
import { MetricsRepository } from "../../data/repositories/MetricsRepository";
import { UserRepository } from "../../data/repositories/UserRepository";
import { Login } from "../../domain/use-cases/auth/Login";
import { Logout } from "../../domain/use-cases/auth/Logout";
import { ValidateSession } from "../../domain/use-cases/auth/ValidateSession";
import { GetCompany } from "../../domain/use-cases/company/GetCompany";
import { UpdateCompany } from "../../domain/use-cases/company/UpdateCompany";
import { AssignConversationToAttendant } from "../../domain/use-cases/conversation/AssignConversationToAttendant";
import { GetConversation } from "../../domain/use-cases/conversation/GetConversation";
import { GetConversationMessages } from "../../domain/use-cases/conversation/GetConversationMessages";
import { GetConversations } from "../../domain/use-cases/conversation/GetConversations";
import { ReceiveMessage } from "../../domain/use-cases/conversation/ReceiveMessage";
import { SearchConversations } from "../../domain/use-cases/conversation/SearchConversations";
import { SendMessage } from "../../domain/use-cases/conversation/SendMessage";
import { CreateCustomer } from "../../domain/use-cases/customer/CreateCustomer";
import { GetCustomersByCompany } from "../../domain/use-cases/customer/GetCustomersByCompany";
import { SearchCustomers } from "../../domain/use-cases/customer/SearchCustomers";
import { GetDashboardMetrics } from "../../domain/use-cases/GetDashboardMetrics";
import { CheckPermission } from "../../domain/use-cases/user/CheckPermission";
import { CreateUser } from "../../domain/use-cases/user/CreateUser";
import { DeleteUser } from "../../domain/use-cases/user/DeleteUser";
import { GetUsersByCompany } from "../../domain/use-cases/user/GetUsersByCompany";
import { SearchUsers } from "../../domain/use-cases/user/SearchUsers";
import { UpdateUser } from "../../domain/use-cases/user/UpdateUser";
import { InMemoryEventBus } from "../events/EventBus";
import { HttpClient } from "../http/HttpClient";
import { WebSocketAdapter } from "../websocket/WebSocketAdapter";
import { onMessageReceivedHandler } from "../websocket/WebSocketHandlers";

// WebSockets
const WS_MESSAGES_URL = "wss://echo.websocket.org";
export const messagesWebSocket = new WebSocketAdapter(WS_MESSAGES_URL);
messagesWebSocket.addHandler(onMessageReceivedHandler);

// EventBus
export const eventBus = new InMemoryEventBus();

// Repositories (Singleton instances)
const conversationRepository = new ConversationRepository();
const metricsRepository = new MetricsRepository();
const client = new HttpClient("http://localhost:8000", 30000, 3);
const companyRepository = new ApiCompanyRepository(client);
const userRepository = new UserRepository();
const authRepository = new AuthRepository(userRepository, companyRepository);
const customerRepository = new ApiCustomerRepository(client);
const attendantStatsRepository = new AttendantStatsRepository();

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

// Metrics Repository (direct access for complex queries)
export { attendantStatsRepository, metricsRepository };

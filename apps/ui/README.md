# Convo UI

React + TypeScript frontend for Convo chat management platform built with Clean Architecture and Domain-Driven Design (DDD) principles.

## Overview

Minimalist messaging/conversation management application that communicates with the Convo API backend and uses WebSocket for real-time messaging.

## Development Commands

```bash
# From this directory (apps/ui/)

# Install dependencies
npm i

# Start development server (http://localhost:3000)
npm run dev

# Build for production (outputs to /build)
npm run build

# Lint code
npm run lint

# Auto-fix linting issues
npm run lint:fix

# Format code with Prettier
npm run format

# Check formatting without modifying
npm run format:check

# Deploy to GitHub Pages
npm run deploy
```

## Architecture

The codebase follows **Clean Architecture** with strict layer separation and inward-pointing dependencies:

```
Presentation Layer (React Components, Hooks)
    ↓
Application Layer (Use Cases)
    ↓
Domain Layer (Entities, Events, Interfaces)
    ↓
Data Layer (Repository Implementations)
    ↓
Infrastructure Layer (HTTP, WebSocket, EventBus, DI Container)
```

### Key Architectural Patterns

1. **Repository Pattern**: All data access goes through repository interfaces defined in `/src/domain/repositories/` and implemented in `/src/data/repositories/`

2. **Dependency Injection**: All use cases and repositories are instantiated in `/src/infrastructure/di/container.ts` and exported as singleton instances

3. **Event-Driven Architecture**: Domain events (defined in `/src/domain/events/`) are published by use cases and consumed by React components via the EventBus

4. **Use Case Pattern**: All business logic is encapsulated in use cases (`/src/domain/use-cases/`) with single responsibility

## Directory Structure

```
/src
├── /components           # Reusable UI components (50+ Radix UI components)
├── /domain              # Domain layer (DDD)
│   ├── /entities        # Business entities (User, Customer, Conversation, etc.)
│   ├── /events          # Domain events (MessageSent, ConversationAssigned, etc.)
│   ├── /ports           # Interface contracts (IEventBus, IWebSocketAdapter)
│   ├── /repositories    # Repository interfaces
│   └── /use-cases       # Application use cases organized by domain
├── /data                # Repository implementations
│   └── /repositories    # Concrete repository classes
├── /infrastructure      # Infrastructure concerns
│   ├── /di              # Dependency injection container
│   ├── /events          # EventBus implementation
│   ├── /http            # HTTP client
│   └── /websocket       # WebSocket adapter
└── /presentation        # Presentation layer
    ├── /components      # Feature-specific React components
    ├── /contexts        # React contexts (AuthContext)
    └── /hooks           # Custom React hooks
```

## Adding New Features

Follow these patterns when adding functionality:

### 1. Define the Entity (if needed)

Create or update entities in `/src/domain/entities/`. Entities are plain TypeScript interfaces representing business objects.

### 2. Define Repository Interface

Add methods to existing repository interfaces in `/src/domain/repositories/` or create a new one following the `I{Name}Repository` pattern.

### 3. Implement Repository

Create or update repository implementation in `/src/data/repositories/`. For API-backed repositories:

- Use `ApiMappers.ts` for DTO transformations
- Use the injected `HttpClient` instance for HTTP calls
- Handle errors consistently

### 4. Create Use Case

Add a new use case class in `/src/domain/use-cases/{domain}/`. Use cases should:

- Accept repository dependencies via constructor
- Have a single `execute()` method
- Publish domain events when state changes occur
- Return domain entities (not DTOs)

### 5. Register in DI Container

Add repository and use case instantiation to `/src/infrastructure/di/container.ts`:

```typescript
// Repository instance
const myRepository = new MyRepository(client);

// Use case instance
export const myUseCase = new MyUseCase(myRepository, eventBus);
```

### 6. Create React Hook (optional)

For complex state management, create a custom hook in `/src/presentation/hooks/`:

- Import use cases from the container
- Subscribe to relevant domain events
- Manage local state with `useState`
- Return data, loading states, and action functions

### 7. Build UI Component

Create React components in `/src/presentation/components/` or `/src/components/ui/` (for reusable primitives).

## Important Patterns

### Event Publishing & Subscription

Use cases publish events through the EventBus:

```typescript
await this.eventBus.publish(new MessageSentEvent(message));
```

React hooks subscribe to events:

```typescript
useEffect(() => {
  const unsubscribe = eventBus.subscribe("MessageReceived", (event) => {
    // Handle event
  });
  return unsubscribe;
}, []);
```

### HTTP Client Usage

The `HttpClient` in `/src/infrastructure/http/HttpClient.ts` provides:

- Automatic JSON serialization
- Configurable timeout (default: 30s)
- Retry logic with exponential backoff
- AbortController for request cancellation

Example repository method:

```typescript
async getById(id: string): Promise<Entity> {
  const response = await this.client.get<EntityDTO>(`/entities/${id}`);
  return ApiMappers.toDomain(response);
}
```

### Path Aliases

The `@` alias resolves to `/src`:

```typescript
import { User } from "@/domain/entities/User";
import { Button } from "@/components/ui/button";
```

## Role-Based Access Control

The app implements RBAC with three roles:

- **ADMINISTRATOR**: Full system access
- **MANAGER**: Company management and reporting
- **ATTENDANT**: Conversation handling only

Check permissions using the `CheckPermission` use case or the `AuthContext`.

## Backend Integration

- **Base URL**: Configured via `VITE_API_BASE_URL` environment variable (defaults to `http://localhost:8000`)
- **WebSocket**: Currently uses `wss://echo.websocket.org` (placeholder)
- **Timeout**: 30 seconds with 3 retries
- **Authentication**: Session-based with AuthRepository

### Repository Migration Strategy

The codebase is transitioning from local/mock repositories to API-backed repositories:

- ✅ `ApiCompanyRepository` - Integrated with backend `/company` endpoints
- ✅ `ApiCustomerRepository` - Integrated with backend `/contacts` endpoints
- 🔄 `ConversationRepository` - Still uses local storage
- 🔄 `UserRepository` - Still uses local storage
- 🔄 `MetricsRepository` - Still uses local storage

When adding new backend endpoints, follow the pattern in `ApiCompanyRepository.ts` and `ApiCustomerRepository.ts`.

## Component Library

UI components use:

- **Radix UI**: Unstyled, accessible component primitives
- **Tailwind CSS**: Utility-first styling (v4)
- **CVA**: Class variance authority for component variants
- **Lucide React**: Icon library
- **Sonner**: Toast notifications
- **react-hook-form**: Form validation and handling

## Styling Guidelines

- Use Tailwind utility classes for all styling
- Color scheme: Primary (green), neutral, amber accents
- Responsive design with mobile-first approach
- Dark mode support via `next-themes`
- Component variants via CVA (see existing components in `/src/components/ui/`)

## Domain Entities

Key entities in the system:

- **User**: System users with roles and permissions
- **Customer**: End users/clients with contact info, tags, and notes
- **Conversation**: Message threads between customers and attendants
- **Message**: Individual messages within conversations
- **Company**: Multi-tenant company configuration
- **AuthSession**: Authentication session data
- **Attendant**: User statistics and metrics
- **Metrics**: Dashboard and reporting data

## Environment Variables

Create `.env` file in this directory:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Docker Deployment

The project includes:

- `Dockerfile` for production builds
- `nginx.conf` for serving the static build
- `build-and-deploy.sh` for Kubernetes deployment

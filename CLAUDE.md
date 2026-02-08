# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this monorepo.

## Project Overview

Convo is a chat management platform consisting of:
- **API** (`apps/api/`): FastAPI backend with Clean Architecture (Python)
- **UI** (`apps/ui/`): React frontend with Clean Architecture (TypeScript)

Both applications follow Clean Architecture principles with strict layer separation.

## Monorepo Structure

```
convo/
├── apps/
│   ├── api/          # FastAPI backend (Python)
│   │   ├── src/      # Source code
│   │   ├── tests/    # Test suites
│   │   └── run_*.py  # Utility scripts
│   └── ui/           # React frontend (TypeScript)
│       ├── src/      # Source code
│       └── k8s/      # Kubernetes manifests
├── scripts/          # Cross-repo scripts
├── docker-compose.yml
└── README.md
```

## Quick Start

```bash
# Start all services (from repository root)
docker compose up

# Access points:
# - Frontend: http://localhost:3000
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

## Git Commit Conventions

Use conventional commit format with app prefixes when relevant:

```
<type>(<scope>): <description>
```

**Types**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

**Scopes** (optional):
- `api`: Backend changes only
- `ui`: Frontend changes only
- Omit scope for changes affecting both or root files

**Examples**:
```
feat(api): add message search endpoint
fix(ui): customer tags validation
chore: update docker-compose configuration
```

**Guidelines**:
- Keep messages concise and descriptive
- Use lowercase for description
- **Do not include** AI assistant co-author attributions
- Focus on **what** changed

---

# API (apps/api/)

## Overview

FastAPI backend managing companies, users, contacts, chats, and messages with webhook integration. Built with Clean Architecture principles.

## Commands

**IMPORTANT:** All `run_*` commands must be executed inside the Docker container:
```bash
docker exec convo_api uv run python <command>
```

### Running the Application
```bash
docker compose up           # Start all services
docker compose down         # Stop all services
```

### Database Seeding
```bash
docker exec convo_api uv run python run_seed_db.py
```

Seeds PostgreSQL with test data (2 companies, 5 users, 6 contacts, 5 chats, 24 messages). Can be re-run safely.

### Testing
```bash
docker exec convo_api uv run python run_tests.py         # Run all tests
docker exec convo_api uv run python run_tests.py -v      # Verbose
docker exec convo_api uv run python run_tests.py tests/unit/  # Specific directory
docker exec convo_api uv run python run_coverage.py      # With coverage
```

### Code Quality
```bash
docker exec convo_api uv run python run_linter.py .      # Check with Ruff
docker exec convo_api uv run python run_linter.py --fix . # Auto-fix
docker exec convo_api uv run python run_formatter.py .   # Format
```

### Deployment
```bash
docker exec convo_api uv run python run_deploy.py        # Deploy to Kubernetes
```

## Architecture

### Domain Layer (`apps/api/src/domain/`)
- **entities/**: Core business entities (User, Company, Contact, Chat, Message)
  - All extend `BaseEntity` with id, created_at, updated_at
  - Immutable dataclasses
- **repositories/**: Repository interfaces (IUserRepository, etc.)
  - Define data access contracts
  - Follow consistent interface pattern: save, get_by_id, get_all, delete
- **errors.py**: Domain-specific exceptions
- **enums.py**: Domain enumerations (UserType, ChatStatus, etc.)

### Application Layer (`apps/api/src/application/`)
- **use_cases/**: Business logic implementation
  - Each use case extends base interface
  - Constructor injection of repositories
  - Single `execute()` method
- **dtos/**: Data transfer objects
- **filters/**: Query filter objects
- **interfaces.py**: Use case base interfaces

### Infrastructure Layer (`apps/api/src/infrastructure/`)
- **repositories/**: Repository implementations (SQLite and PostgreSQL)
  - `sqlite_*_repository.py`: SQLite implementations
  - `postgres_*_repository.py`: PostgreSQL implementations
- **daos/**: Data Access Objects for direct database interaction
  - `*_dao.py`: SQLite DAOs
  - `postgres_*_dao.py`: PostgreSQL DAOs
- **database/**: Database setup and migrations
  - `create_sqlite_tables.sql`: SQLite schema
  - `create_postgres_tables.sql`: PostgreSQL schema
  - `sqlite_setup.py`: Type converters
  - `postgres_setup.py`: Connection factory
  - `init_postgres_db.py`: Database initialization
- **repository_factory.py**: Creates repositories based on database type
- **enums.py**: Infrastructure enumerations (DatabaseType)
- **settings.py**: Application configuration

### Web Layer (`apps/api/src/web/`)
- **controllers/**: HTTP controllers
  - Return framework-agnostic HttpResponse objects
- **framework/**: FastAPI-specific implementation
  - `app.py`: FastAPI app factory with dependency injection
  - `routes/`: Route definitions
  - `adapter.py`: Request type conversion
- **http_types.py**: Framework-agnostic HTTP types

## API Key Patterns

### Dependency Injection
```python
# In app.py
app.state.user_repository = InMemoryUserRepository()

# In routes
repository = request.app.state.user_repository
controller = ListUserHttpController(user_repository=repository)
```

### Request Adaptation
```python
from src.web.framework.adapter import request_adapter
response = controller.handle(request=await request_adapter(request))
```

### Database Selection
Controlled by `DATABASE_TYPE` environment variable:
- `inmemory`: In-memory repositories (default, testing)
- `sqlite`: SQLite database (local development)
- `postgres`: PostgreSQL database (production)

## API Testing Structure

- **tests/unit/**: Unit tests with fake repositories
  - `application/use_cases/`: Use case tests
  - `domain/`: Entity tests
- **tests/integration/**: Integration tests
  - `web/framework/routes/`: HTTP endpoint tests
  - `infrastructure/`: Database operation tests
- **tests/fixtures/**: Pytest fixtures
- **tests/factories/**: Test entity factories
- **tests/fakes/**: In-memory repositories

## API Environment Variables

Required in `apps/api/.env`:
- `DATABASE_TYPE`: Database backend (`inmemory`, `sqlite`, `postgres`)
- `DATABASE_NAME`: Database file/name
- `DATABASE_USER`: Database user (PostgreSQL)
- `DATABASE_PASSWORD`: Database password (PostgreSQL)
- `DATABASE_URL`: Full connection URL
- `WEBHOOK_VERIFY_TOKEN`: Webhook verification token
- `CORS_ORIGINS`: Comma-separated allowed origins

See `apps/api/.env.example` for templates.

## Adding API Features

1. **Domain Layer**: Create entity in `src/domain/entities/` and repository interface in `src/domain/repositories/`
2. **Infrastructure Layer**: Implement DAO in `src/infrastructure/daos/` and repository in `src/infrastructure/repositories/`
3. **Application Layer**: Create use cases in `src/application/use_cases/`
4. **Web Layer**: Add controllers and routes
5. **Testing**: Create fake repository and tests
6. **Database**: Update both SQL schema files
7. **Repository Factory**: Update `src/infrastructure/repository_factory.py`

## API Code Style

- Uses Ruff for linting and formatting
- Line length: 88 characters
- Python 3.13+ required
- Print statements allowed only in run_* scripts

---

# UI (apps/ui/)

## Overview

React + TypeScript frontend with Clean Architecture and Domain-Driven Design. Communicates with API backend and uses WebSocket for real-time messaging.

## Commands

**Run from `apps/ui/` directory:**

```bash
npm i                    # Install dependencies
npm run dev              # Start dev server (http://localhost:3000)
npm run build            # Build for production
npm run lint             # Lint code
npm run lint:fix         # Auto-fix linting
npm run format           # Format with Prettier
npm run format:check     # Check formatting
npm run deploy           # Deploy to GitHub Pages
```

## Architecture

Clean Architecture with inward-pointing dependencies:

```
Presentation (React Components, Hooks)
    ↓
Application (Use Cases)
    ↓
Domain (Entities, Events, Interfaces)
    ↓
Data (Repository Implementations)
    ↓
Infrastructure (HTTP, WebSocket, EventBus, DI)
```

### UI Key Patterns

1. **Repository Pattern**: Interfaces in `/src/domain/repositories/`, implementations in `/src/data/repositories/`
2. **Dependency Injection**: All instances in `/src/infrastructure/di/container.ts`
3. **Event-Driven**: Domain events published by use cases, consumed by React components
4. **Use Case Pattern**: Business logic in `/src/domain/use-cases/`

## UI Directory Structure

```
/src
├── /components           # Reusable UI components (Radix UI)
├── /domain              # Domain layer
│   ├── /entities        # Business entities
│   ├── /events          # Domain events
│   ├── /ports           # Interface contracts
│   ├── /repositories    # Repository interfaces
│   └── /use-cases       # Application use cases
├── /data                # Repository implementations
├── /infrastructure      # Infrastructure concerns
│   ├── /di              # DI container
│   ├── /events          # EventBus
│   ├── /http            # HTTP client
│   └── /websocket       # WebSocket adapter
└── /presentation        # Presentation layer
    ├── /components      # Feature components
    ├── /contexts        # React contexts
    └── /hooks           # Custom hooks
```

## Adding UI Features

1. **Define Entity**: Create/update in `/src/domain/entities/`
2. **Define Repository Interface**: In `/src/domain/repositories/`
3. **Implement Repository**: In `/src/data/repositories/`
4. **Create Use Case**: In `/src/domain/use-cases/{domain}/`
5. **Register in DI Container**: In `/src/infrastructure/di/container.ts`
6. **Create React Hook**: In `/src/presentation/hooks/` (optional)
7. **Build UI Component**: In `/src/presentation/components/` or `/src/components/ui/`

## UI Important Patterns

### Event Publishing
```typescript
await this.eventBus.publish(new MessageSentEvent(message));
```

### Event Subscription
```typescript
useEffect(() => {
  const unsubscribe = eventBus.subscribe('MessageReceived', (event) => {
    // Handle event
  });
  return unsubscribe;
}, []);
```

### HTTP Client Usage
```typescript
async getById(id: string): Promise<Entity> {
  const response = await this.client.get<EntityDTO>(`/entities/${id}`);
  return ApiMappers.toDomain(response);
}
```

### Path Aliases
```typescript
import { User } from '@/domain/entities/User';
import { Button } from '@/components/ui/button';
```

## Role-Based Access Control

Three roles:
- **ADMINISTRATOR**: Full system access
- **MANAGER**: Company management and reporting
- **ATTENDANT**: Conversation handling only

## Backend Integration

- **Base URL**: `VITE_API_BASE_URL` env var (defaults to `http://localhost:8000`)
- **WebSocket**: Currently `wss://echo.websocket.org` (placeholder)
- **Timeout**: 30 seconds with 3 retries
- **Authentication**: Session-based

### Repository Migration Status

- ✅ `ApiCompanyRepository` - Integrated
- ✅ `ApiCustomerRepository` - Integrated
- 🔄 `ConversationRepository` - Local storage
- 🔄 `UserRepository` - Local storage
- 🔄 `MetricsRepository` - Local storage

## Component Library

- **Radix UI**: Accessible component primitives
- **Tailwind CSS**: Utility-first styling (v4)
- **CVA**: Component variants
- **Lucide React**: Icons
- **Sonner**: Toast notifications
- **react-hook-form**: Form handling

## Styling Guidelines

- Use Tailwind utility classes
- Color scheme: Primary (green), neutral, amber accents
- Mobile-first responsive design
- Dark mode support via `next-themes`

## UI Environment Variables

Create `apps/ui/.env`:
```env
VITE_API_BASE_URL=http://localhost:8000
```

## Domain Entities

- **User**: System users with roles
- **Customer**: End users/clients
- **Conversation**: Message threads
- **Message**: Individual messages
- **Company**: Multi-tenant configuration
- **AuthSession**: Authentication data
- **Attendant**: User statistics
- **Metrics**: Dashboard data

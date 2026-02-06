# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Convo is a conversation/chat management API built with FastAPI following Clean Architecture principles. The system manages companies, users, contacts, chats, and messages with webhook integration.

## Commands

### Running the Application
```bash
python main.py              # Run development server with hot reload
```

### Testing
```bash
python run_tests.py         # Run all tests with pytest
python run_tests.py -v      # Run with verbose output
python run_tests.py tests/unit/  # Run specific test directory
python run_tests.py tests/unit/application/use_cases/test_user_use_case.py  # Run single test file
python run_tests.py -k test_name  # Run tests matching pattern
python run_coverage.py      # Run tests with coverage report
```

### Code Quality
```bash
python run_linter.py .      # Check code with Ruff
python run_linter.py --fix . # Auto-fix linting issues
python run_formatter.py .   # Format code with Ruff
python run_formatter.py --check .  # Check formatting without changes
```

### Deployment
```bash
python run_deploy.py        # Build Docker image and deploy to Kubernetes
```

## Architecture

This project follows Clean Architecture with clear layer separation:

### Domain Layer (`src/domain/`)
- **entities/**: Core business entities (User, Company, Contact, Chat, Message)
  - All entities extend `BaseEntity` with id, created_at, updated_at
  - Entities are immutable dataclasses
- **repositories/**: Repository interfaces (IUserRepository, etc.)
  - Define contracts for data access
  - All repositories follow same interface pattern: save, get_by_id, get_all, delete
- **errors.py**: Domain-specific exceptions
- **enums.py**: Domain enumerations (UserType, ChatStatus, etc.)

### Application Layer (`src/application/`)
- **use_cases/**: Business logic implementation
  - Each use case extends base interface (IUserUseCase, ICompanyUseCase, etc.)
  - Use cases receive repositories through constructor injection
  - All use cases implement execute() method
- **dtos/**: Data transfer objects for use case input/output
- **filters/**: Query filter objects
- **interfaces.py**: Use case base interfaces

### Infrastructure Layer (`src/infrastructure/`)
- **repositories/**: Repository implementations (SQLiteUserRepository, etc.)
  - Implement domain repository interfaces
  - Depend on DAOs for database operations
- **daos/**: Data Access Objects for direct database interaction
  - Handle raw SQL queries
  - Convert between database rows and dictionaries
- **database/**: Database setup and migrations
  - `create_tables.sql`: Database schema
  - `sqlite_setup.py`: SQLite type converters for Python types
- **settings.py**: Application configuration from environment variables

### Web Layer (`src/web/`)
- **controllers/**: HTTP controllers implementing business operations
  - Each controller extends base interface (IUserHttpController, etc.)
  - Receive repositories through constructor injection
  - Return HttpResponse objects (framework-agnostic)
- **framework/**: FastAPI-specific implementation
  - `app.py`: FastAPI app factory with repository injection
  - `routes/`: FastAPI route definitions
  - `adapter.py`: Converts FastAPI Request to internal HttpRequest type
- **http_types.py**: Framework-agnostic HTTP types (HttpRequest, HttpResponse)

## Key Patterns

### Dependency Injection
Repositories are injected through `app.state` in FastAPI:
```python
# In app.py
app.state.user_repository = InMemoryUserRepository()

# In routes
repository = request.app.state.user_repository
controller = ListUserHttpController(user_repository=repository)
```

### Request Adaptation
FastAPI requests are converted to internal HttpRequest type:
```python
from src.web.framework.adapter import request_adapter

response = controller.handle(request=await request_adapter(request))
```

### Repository Pattern
- Domain defines interfaces in `src/domain/repositories/`
- Infrastructure provides SQLite implementations in `src/infrastructure/repositories/`
- Tests use fake in-memory implementations from `tests/fakes/repositories/`

### Current Repository State
The app is currently using in-memory repositories (defined in tests/fakes/). SQLite implementations exist but are commented out in app.py:55-56. To switch to SQLite:
1. Uncomment SQLite repository setup in `src/web/framework/app.py`
2. Comment out the in-memory repository lines

## Testing Structure

- **tests/unit/**: Unit tests for business logic
  - `application/use_cases/`: Test use cases with fake repositories
  - `domain/`: Test domain entities
- **tests/integration/**: Integration tests
  - `web/framework/routes/`: Test HTTP endpoints with TestClient
  - `infrastructure/`: Test database operations
- **tests/fixtures/**: Pytest fixtures for repositories, databases, and web clients
- **tests/factories/**: Factory functions for creating test entities
- **tests/fakes/**: In-memory repository implementations for testing
- **conftest.py**: Auto-imports all fixtures and factories

## Database Schema

Main entities and relationships:
- **companies**: Root entity for multi-tenancy
- **users**: Belong to companies, can be attendants
- **contacts**: External contacts (customers) linked to companies
- **chats**: Conversations between company and contact, can be attached to user
- **messages**: Individual messages in chats

All tables use TEXT primary keys (UUIDs) and include created_at/updated_at timestamps.

## Environment Variables

Required in `.env` file:
- `DATABASE_NAME`: Database file name
- `DATABASE_USER`: Database user
- `DATABASE_PASSWORD`: Database password
- `DATABASE_URL`: Full database connection URL
- `WEBHOOK_VERIFY_TOKEN`: Token for webhook verification
- `CORS_ORIGINS`: Comma-separated list of allowed origins

## Adding New Features

When adding a new entity or feature:

1. **Domain Layer**: Create entity in `src/domain/entities/` and repository interface in `src/domain/repositories/`
2. **Infrastructure Layer**: Implement DAO in `src/infrastructure/daos/` and repository in `src/infrastructure/repositories/`
3. **Application Layer**: Create use cases in `src/application/use_cases/`
4. **Web Layer**:
   - Add controllers in `src/web/controllers/`
   - Add routes in `src/web/framework/routes/`
   - Register router in `src/web/framework/app.py`
5. **Testing**:
   - Create fake repository in `tests/fakes/repositories/`
   - Add unit tests in `tests/unit/`
   - Add integration tests in `tests/integration/`
6. **Database**: Update `src/infrastructure/database/create_tables.sql` if needed

## Code Style

- Uses Ruff for linting and formatting (configured in pyproject.toml)
- Line length: 88 characters
- Python 3.13+ required
- Imports sorted automatically by Ruff
- Print statements allowed only in run_* scripts

## Git Commit Conventions

- Use conventional commit format: `type: description`
- Common types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- **Do not include** AI assistant co-author attributions (e.g., "Co-Authored-By") in commit messages
- Keep commit messages concise and descriptive

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Convo is a conversation/chat management API built with FastAPI following Clean Architecture principles. The system manages companies, users, contacts, chats, and messages with webhook integration.

## Commands

**IMPORTANT:** All `run_*` commands must be executed inside the Docker container using the pattern:
```bash
docker exec convo_api uv run python <command>
```

### Running the Application
```bash
docker compose up           # Start all services (API, database, ngrok)
docker compose down         # Stop all services
```

### Testing
```bash
docker exec convo_api uv run python run_tests.py         # Run all tests with pytest
docker exec convo_api uv run python run_tests.py -v      # Run with verbose output
docker exec convo_api uv run python run_tests.py tests/unit/  # Run specific test directory
docker exec convo_api uv run python run_tests.py tests/unit/application/use_cases/test_user_use_case.py  # Run single test file
docker exec convo_api uv run python run_tests.py -k test_name  # Run tests matching pattern
docker exec convo_api uv run python run_coverage.py      # Run tests with coverage report
```

### Code Quality
```bash
docker exec convo_api uv run python run_linter.py .      # Check code with Ruff
docker exec convo_api uv run python run_linter.py --fix . # Auto-fix linting issues
docker exec convo_api uv run python run_formatter.py .   # Format code with Ruff
docker exec convo_api uv run python run_formatter.py --check .  # Check formatting without changes
```

### Deployment
```bash
docker exec convo_api uv run python run_deploy.py        # Build Docker image and deploy to Kubernetes
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
- **repositories/**: Repository implementations (SQLite and PostgreSQL)
  - Implement domain repository interfaces
  - Depend on DAOs for database operations
  - `sqlite_*_repository.py`: SQLite implementations
  - `postgres_*_repository.py`: PostgreSQL implementations
- **daos/**: Data Access Objects for direct database interaction
  - Handle raw SQL queries
  - Convert between database rows and dictionaries
  - `*_dao.py`: SQLite DAOs
  - `postgres_*_dao.py`: PostgreSQL DAOs
- **database/**: Database setup and migrations
  - `create_sqlite_tables.sql`: SQLite database schema
  - `create_postgres_tables.sql`: PostgreSQL database schema
  - `sqlite_setup.py`: SQLite type converters for Python types
  - `postgres_setup.py`: PostgreSQL connection factory
  - `init_postgres_db.py`: PostgreSQL database initialization script
- **repository_factory.py**: Factory for creating repositories based on database type
- **enums.py**: Infrastructure enumerations (DatabaseType)
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
- Infrastructure provides multiple implementations:
  - SQLite repositories in `src/infrastructure/repositories/sqlite_*_repository.py`
  - PostgreSQL repositories in `src/infrastructure/repositories/postgres_*_repository.py`
- Tests use fake in-memory implementations from `tests/fakes/repositories/`
- Repository selection is handled by `repository_factory.py` based on `DATABASE_TYPE` environment variable

### Database Selection
The application supports three database backends controlled by the `DATABASE_TYPE` environment variable (defined in `DatabaseType` enum in `src/infrastructure/enums.py`):
- `inmemory`: In-memory repositories (default, for development/testing)
- `sqlite`: SQLite database (for local development)
- `postgres`: PostgreSQL database (for production)

The repository factory (`src/infrastructure/repository_factory.py`) automatically creates the appropriate repository implementations based on this setting. Invalid database types will raise a `ValueError` with available options.

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

**Schema files:**
- `src/infrastructure/database/create_sqlite_tables.sql`: SQLite schema
- `src/infrastructure/database/create_postgres_tables.sql`: PostgreSQL schema with timezone-aware timestamps

**Key differences between SQLite and PostgreSQL schemas:**
- Boolean defaults: SQLite uses `0`/`1`, PostgreSQL uses `FALSE`/`TRUE`
- Timestamps: PostgreSQL uses `TIMESTAMP WITH TIME ZONE` for better timezone handling
- Foreign keys: Both support foreign key constraints natively

## Environment Variables

Required in `.env` file:
- `DATABASE_TYPE`: Database backend type (`inmemory`, `sqlite`, or `postgres`) - defaults to `inmemory`
- `DATABASE_NAME`: Database file name (for SQLite) or database name (for PostgreSQL)
- `DATABASE_USER`: Database user (for PostgreSQL)
- `DATABASE_PASSWORD`: Database password (for PostgreSQL)
- `DATABASE_URL`: Full database connection URL
  - SQLite format: `sqlite:///app.db`
  - PostgreSQL format: `postgresql://user:password@host:port/database`
- `WEBHOOK_VERIFY_TOKEN`: Token for webhook verification
- `CORS_ORIGINS`: Comma-separated list of allowed origins

### Database Configuration Examples

**For SQLite (local development):**
```env
DATABASE_TYPE=sqlite
DATABASE_NAME=app.db
DATABASE_URL=sqlite:///app.db
DATABASE_USER=
DATABASE_PASSWORD=
```

**For PostgreSQL (production):**
```env
DATABASE_TYPE=postgres
DATABASE_NAME=convo_db
DATABASE_USER=convo_user
DATABASE_PASSWORD=secure_password
DATABASE_URL=postgresql://convo_user:secure_password@localhost:5432/convo_db
```

**For In-Memory (testing/development):**
```env
DATABASE_TYPE=inmemory
# Other DATABASE_* variables not required
```

### PostgreSQL Database Initialization

To initialize the PostgreSQL database with the schema:
```bash
# Set DATABASE_URL environment variable first
export DATABASE_URL=postgresql://user:password@host:port/database

# Run initialization script
python src/infrastructure/database/init_postgres_db.py
```

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
6. **Database**: Update both `create_sqlite_tables.sql` and `create_postgres_tables.sql` if schema changes are needed
7. **Repository Factory**: Update `src/infrastructure/repository_factory.py` to include new repositories

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

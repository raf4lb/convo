# Convo - Chat Management Platform

Monorepo containing the Convo chat management platform with both API and UI.

## Project Structure

```
convo/
├── apps/
│   ├── api/          # FastAPI backend (Python)
│   └── ui/           # React frontend (TypeScript)
├── scripts/          # Cross-repo scripts
├── docker-compose.yml
└── CLAUDE.md         # Development guide for AI assistants
```

## Quick Start

1. Copy environment variables:
   ```bash
   cp apps/api/.env.example apps/api/.env
   # Edit apps/api/.env with your configuration
   ```

2. Start all services:
   ```bash
   docker compose up
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Ngrok Dashboard: http://localhost:4040

## Services

- **API** - FastAPI backend with Clean Architecture
- **UI** - React frontend with TypeScript
- **DB** - PostgreSQL 18 database
- **Ngrok** - HTTP tunneling for webhook testing

## Development

Each app has its own development workflow:

- **API Documentation**: [apps/api/README.md](./apps/api/README.md)
- **UI Documentation**: [apps/ui/README.md](./apps/ui/README.md)
- **Full Development Guide**: [CLAUDE.md](./CLAUDE.md)

## Common Commands

```bash
# Start all services
docker compose up

# Stop all services
docker compose down

# Rebuild containers
docker compose up --build

# View logs
docker compose logs -f

# View specific service logs
docker compose logs -f api
docker compose logs -f ui
```

## Architecture

This monorepo follows Clean Architecture principles in both applications:

- **Domain Layer**: Core business entities and rules
- **Application Layer**: Use cases and business logic
- **Infrastructure Layer**: Database, external services
- **Web/Presentation Layer**: HTTP controllers and UI components

See individual app READMEs for detailed architecture documentation.

## Testing

```bash
# Run API tests
docker exec convo_api uv run python run_tests.py

# Run API tests with coverage
docker exec convo_api uv run python run_coverage.py

# Run UI tests (from apps/ui directory)
cd apps/ui
npm test
```

## Code Quality

```bash
# API linting and formatting
docker exec convo_api uv run python run_linter.py .
docker exec convo_api uv run python run_formatter.py .

# UI linting and formatting
cd apps/ui
npm run lint
npm run format
```

## Database

The application uses PostgreSQL with automatic initialization:

```bash
# Seed database with test data
docker exec convo_api uv run python run_seed_db.py
```

## License

MIT

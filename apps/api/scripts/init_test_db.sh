#!/bin/bash
# Create/reset test database in PostgreSQL container
# Called automatically by run_tests.py unless --no-db flag is used

set -e  # Exit on error

echo "Setting up test database..."

# Create test database (drop if exists)
docker exec convo_db psql -U convo_user -d postgres -c "DROP DATABASE IF EXISTS convo_test_db;" 2>/dev/null || true
docker exec convo_db psql -U convo_user -d postgres -c "CREATE DATABASE convo_test_db;"

echo "Test database created. Schema will initialize on first test run."

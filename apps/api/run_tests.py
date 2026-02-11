#!/usr/bin/env python3
"""
Script para rodar pytest programaticamente.
Equivalente a executar: python -m pytest
Compatível com Windows, macOS e Linux.

Automatically sets up test database before running tests unless --no-db flag is used.
"""

import subprocess
import sys
from pathlib import Path

import pytest


def setup_test_database():
    """
    Initialize test database by running setup_test_db.py script.

    The script creates/resets the test database (convo_test_db) to ensure
    a clean state for integration tests. Schema initialization happens
    automatically on first test run via the test_database_url fixture.
    """
    script_path = Path(__file__).parent / "scripts" / "setup_test_db.py"

    if not script_path.exists():
        print(f"Warning: Test database setup script not found at {script_path}")
        print("Skipping database setup. DAO tests may fail.")
        return

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=False,  # Don't raise exception, just continue
            capture_output=True,
            text=True,
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        if result.returncode != 0:
            print("Test database setup had issues. DAO tests may fail.")
    except Exception as e:
        print(f"Error setting up test database: {e}")
        print("Continuing with tests. DAO tests may fail.")


def main():
    """
    Run pytest with automatic test database setup.

    Usage:
        python run_tests.py                    # Run with database setup
        python run_tests.py --no-db            # Skip database setup (unit tests)
        python run_tests.py -v                 # Verbose mode with database setup
        python run_tests.py --no-db -v         # Verbose mode without database

    The --no-db flag skips test database creation/reset, which is useful for
    running only unit tests that don't require database access.
    """
    args = sys.argv[1:]

    # Check for --no-db flag
    skip_db = "--no-db" in args
    if skip_db:
        args.remove("--no-db")

    # Setup test database if not skipped
    if not skip_db:
        setup_test_database()

    # Run pytest with remaining args
    exit_code = pytest.main(args)

    # Exit with pytest's exit code
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

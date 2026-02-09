from enum import Enum


class DatabaseType(str, Enum):
    """Supported database backend types."""

    INMEMORY = "inmemory"
    POSTGRES = "postgres"

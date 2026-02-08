import sqlite3


def init_db(db_path="app.db"):
    schema_file = "src/infrastructure/database/create_sqlite_tables.sql"
    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        with open(schema_file, encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()
    print(f"✅ Banco de dados inicializado em {db_path}")


if __name__ == "__main__":
    init_db(db_path="app.db")

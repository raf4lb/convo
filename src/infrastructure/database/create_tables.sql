CREATE TABLE IF NOT EXISTS companies (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    whatsapp_api_key TEXT,
    is_active BOOLEAN DEFAULT 1 NOT NULL,
    attendant_sees_all_conversations BOOLEAN DEFAULT 1 NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL,
    company_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

CREATE TABLE IF NOT EXISTS contacts (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    company_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS chats (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    contact_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'open',
    attached_user_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (contact_id) REFERENCES contacts(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
    FOREIGN KEY (attached_user_id) REFERENCES users(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    external_id TEXT NOT NULL,
    external_timestamp TIMESTAMP NOT NULL,
    chat_id TEXT NOT NULL,
    is_received INTEGER NOT NULL CHECK (is_received IN (0, 1)),
    text TEXT NOT NULL,
    received_by TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    FOREIGN KEY (chat_id) REFERENCES chats(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (received_by) REFERENCES contacts(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

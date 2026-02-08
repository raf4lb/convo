-- Seed script for PostgreSQL database
-- Populates the database with test data from fake repositories
-- Can be re-run safely with ON CONFLICT DO NOTHING

-- Clear existing data (optional, for clean re-seeding)
-- Uncomment the line below to clear data before seeding
-- TRUNCATE TABLE messages, chats, contacts, users, companies CASCADE;

-- Insert companies
INSERT INTO companies (id, name, email, phone, whatsapp_api_key, is_active, attendant_sees_all_conversations, created_at, updated_at)
VALUES
    ('474d2fd7-2e99-452b-a4db-fe93ecf8729c', 'Tech Solutions Ltda', 'contato@techsolutions.com', '5511987654321', 'mock-api-key-123', TRUE, TRUE, '2024-01-15 00:00:00+00', '2024-01-15 00:00:00+00'),
    ('6dfaada5-37b1-442d-a21b-b63edf12bbd0', 'Comércio Digital SA', 'contato@comerciodigital.com', '5521998765432', 'mock-api-key-456', TRUE, FALSE, '2024-02-20 00:00:00+00', '2024-02-20 00:00:00+00')
ON CONFLICT (id) DO NOTHING;

-- Insert users (password for all: Password123)
INSERT INTO users (id, name, email, type, password_hash, company_id, is_active, created_at, updated_at)
VALUES
    ('03f1d919-cba6-479f-baec-5fcbc77b9d85', 'Admin User', 'admin@techsolutions.com', 'administrator', '$2b$12$K1VscGyaJdHcN5lioNvm9ugNt1Z4h9D3I5BCQt4w/RVpsNE68W3NC', '474d2fd7-2e99-452b-a4db-fe93ecf8729c', TRUE, '2024-01-15 00:00:00+00', NULL),
    ('e8bf801b-d16a-4736-8df9-df9d9278293c', 'João Silva', 'joao@techsolutions.com', 'staff', '$2b$12$K1VscGyaJdHcN5lioNvm9ugNt1Z4h9D3I5BCQt4w/RVpsNE68W3NC', '474d2fd7-2e99-452b-a4db-fe93ecf8729c', TRUE, '2024-01-20 00:00:00+00', NULL),
    ('3b757f19-4cba-448a-b114-31d54c53adf9', 'Ana Costa', 'ana@techsolutions.com', 'staff', '$2b$12$K1VscGyaJdHcN5lioNvm9ugNt1Z4h9D3I5BCQt4w/RVpsNE68W3NC', '474d2fd7-2e99-452b-a4db-fe93ecf8729c', TRUE, '2024-01-20 00:00:00+00', NULL),
    ('23d04704-3770-4e4e-b5fe-b73359a400f5', 'Carlos Mendes', 'carlos@techsolutions.com', 'manager', '$2b$12$K1VscGyaJdHcN5lioNvm9ugNt1Z4h9D3I5BCQt4w/RVpsNE68W3NC', '474d2fd7-2e99-452b-a4db-fe93ecf8729c', TRUE, '2024-01-18 00:00:00+00', NULL),
    ('b7b5c158-355d-45c2-b021-7e1bdbdd0f87', 'Admin Comércio', 'admin@comerciodigital.com', 'administrator', '$2b$12$K1VscGyaJdHcN5lioNvm9ugNt1Z4h9D3I5BCQt4w/RVpsNE68W3NC', '6dfaada5-37b1-442d-a21b-b63edf12bbd0', TRUE, '2024-02-20 00:00:00+00', NULL)
ON CONFLICT (id) DO NOTHING;

-- Insert contacts
INSERT INTO contacts (id, name, phone_number, email, company_id, is_blocked, tags, notes, last_contact_at, created_at, updated_at)
VALUES
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc085', 'Maria Silva', '5511987654321', 'maria.silva@email.com', '474d2fd7-2e99-452b-a4db-fe93ecf8729c', FALSE, 'VIP,Cliente Recorrente', 'Cliente muito importante, sempre compra produtos premium', '2024-11-12 10:30:00+00', '2024-01-10 00:00:00+00', NULL),
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc086', 'Carlos Santos', '5521998765432', 'carlos.santos@email.com', '474d2fd7-2e99-452b-a4db-fe93ecf8729c', FALSE, 'Novo Cliente', NULL, '2024-11-12 09:15:00+00', '2024-02-15 00:00:00+00', NULL),
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc087', 'Fernanda Lima', '5511912345678', NULL, '474d2fd7-2e99-452b-a4db-fe93ecf8729c', FALSE, 'Interessado', NULL, '2024-11-11 14:20:00+00', '2024-03-20 00:00:00+00', NULL),
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc088', 'Pedro Oliveira', '5511988887777', 'pedro.oliveira@email.com', '474d2fd7-2e99-452b-a4db-fe93ecf8729c', FALSE, NULL, NULL, '2024-11-11 16:45:00+00', '2024-04-05 00:00:00+00', NULL),
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc089', 'Julia Costa', '5521977776666', 'julia.costa@email.com', '474d2fd7-2e99-452b-a4db-fe93ecf8729c', FALSE, 'Urgente', 'Precisa de atendimento prioritário', '2024-11-12 11:45:00+00', '2024-05-12 00:00:00+00', NULL),
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc090', 'Antônio Alves', '5511955554444', 'antonio.alves@email.com', '6dfaada5-37b1-442d-a21b-b63edf12bbd0', FALSE, NULL, NULL, '2024-11-10 10:00:00+00', '2024-02-25 00:00:00+00', NULL)
ON CONFLICT (id) DO NOTHING;

-- Insert chats
INSERT INTO chats (id, company_id, contact_id, status, attached_user_id, created_at, updated_at)
VALUES
    ('f4bf4e4e-935a-4fae-a6a5-e65292decc74', '474d2fd7-2e99-452b-a4db-fe93ecf8729c', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc085', 'pending', 'e8bf801b-d16a-4736-8df9-df9d9278293c', '2024-11-12 10:00:00+00', '2024-11-12 10:30:00+00'),
    ('2ef42cf2-24d6-4553-bb79-614558549602', '474d2fd7-2e99-452b-a4db-fe93ecf8729c', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc086', 'open', '3b757f19-4cba-448a-b114-31d54c53adf9', '2024-11-12 09:00:00+00', '2024-11-12 09:15:00+00'),
    ('4e018edb-8219-445a-9bc1-9c8ddbf76da7', '474d2fd7-2e99-452b-a4db-fe93ecf8729c', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc087', 'pending', NULL, '2024-11-11 14:00:00+00', '2024-11-11 14:20:00+00'),
    ('dbfd6c8a-41e3-4e95-b575-921983cea167', '474d2fd7-2e99-452b-a4db-fe93ecf8729c', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc088', 'closed', 'e8bf801b-d16a-4736-8df9-df9d9278293c', '2024-11-11 16:00:00+00', '2024-11-11 16:45:00+00'),
    ('948ed322-a961-46fd-b533-363103e94d3a', '474d2fd7-2e99-452b-a4db-fe93ecf8729c', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc089', 'pending', NULL, '2024-11-12 11:30:00+00', '2024-11-12 11:45:00+00')
ON CONFLICT (id) DO NOTHING;

-- Insert messages
INSERT INTO messages (id, external_id, external_timestamp, chat_id, text, sent_by_user_id, created_at, updated_at)
VALUES
    -- Chat 1: Maria Silva (f4bf4e4e-935a-4fae-a6a5-e65292decc74)
    ('c20d1bfb-b570-4014-8756-4737a50ca76d', 'c20d1bfb-b570-4014-8756-4737a50ca76d', '2024-11-12 10:28:00+00', 'f4bf4e4e-935a-4fae-a6a5-e65292decc74', 'Olá! Gostaria de saber mais sobre os produtos', NULL, '2024-11-12 10:28:00+00', NULL),
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc062', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc062', '2024-11-12 10:29:00+00', 'f4bf4e4e-935a-4fae-a6a5-e65292decc74', 'Olá Maria! Claro, ficarei feliz em ajudar. Temos diversas opções disponíveis.', 'e8bf801b-d16a-4736-8df9-df9d9278293c', '2024-11-12 10:29:00+00', NULL),
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc063', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc063', '2024-11-12 10:29:30+00', 'f4bf4e4e-935a-4fae-a6a5-e65292decc74', 'Vocês fazem entrega?', NULL, '2024-11-12 10:29:30+00', NULL),
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc064', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc064', '2024-11-12 10:30:00+00', 'f4bf4e4e-935a-4fae-a6a5-e65292decc74', 'Sim! Fazemos entregas para toda a cidade. O prazo varia de 2 a 5 dias úteis.', 'e8bf801b-d16a-4736-8df9-df9d9278293c', '2024-11-12 10:30:00+00', NULL),
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc065', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc065', '2024-11-12 10:30:30+00', 'f4bf4e4e-935a-4fae-a6a5-e65292decc74', 'Gostaria de saber mais sobre os produtos', NULL, '2024-11-12 10:30:30+00', NULL),
    -- Chat 2: Carlos Santos (2ef42cf2-24d6-4553-bb79-614558549602)
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc066', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc066', '2024-11-12 09:00:00+00', '2ef42cf2-24d6-4553-bb79-614558549602', 'Bom dia! Gostaria de fazer uma reclamação sobre o produto', NULL, '2024-11-12 09:00:00+00', NULL),
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc067', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc067', '2024-11-12 09:05:00+00', '2ef42cf2-24d6-4553-bb79-614558549602', 'Bom dia, Carlos! Sinto muito pelo inconveniente. Pode me contar o que aconteceu?', '3b757f19-4cba-448a-b114-31d54c53adf9', '2024-11-12 09:05:00+00', NULL),
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc068', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc068', '2024-11-12 09:07:00+00', '2ef42cf2-24d6-4553-bb79-614558549602', 'O produto chegou com defeito', NULL, '2024-11-12 09:07:00+00', NULL),
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc069', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc069', '2024-11-12 09:10:00+00', '2ef42cf2-24d6-4553-bb79-614558549602', 'Entendo. Vou providenciar a troca imediatamente. Pode me enviar uma foto?', '3b757f19-4cba-448a-b114-31d54c53adf9', '2024-11-12 09:10:00+00', NULL),
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc070', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc070', '2024-11-12 09:12:00+00', '2ef42cf2-24d6-4553-bb79-614558549602', 'Claro, vou enviar agora', NULL, '2024-11-12 09:12:00+00', NULL),
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc071', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc071', '2024-11-12 09:14:00+00', '2ef42cf2-24d6-4553-bb79-614558549602', 'Perfeito! Já estou abrindo o chamado de troca. Você receberá o produto novo em até 3 dias úteis.', '3b757f19-4cba-448a-b114-31d54c53adf9', '2024-11-12 09:14:00+00', NULL),
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc072', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc072', '2024-11-12 09:15:00+00', '2ef42cf2-24d6-4553-bb79-614558549602', 'Obrigado pelo atendimento!', NULL, '2024-11-12 09:15:00+00', NULL),
    -- Chat 3: Fernanda Lima (4e018edb-8219-445a-9bc1-9c8ddbf76da7)
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc073', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc073', '2024-11-11 14:18:00+00', '4e018edb-8219-445a-9bc1-9c8ddbf76da7', 'Olá!', NULL, '2024-11-11 14:18:00+00', NULL),
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc074', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc074', '2024-11-11 14:20:00+00', '4e018edb-8219-445a-9bc1-9c8ddbf76da7', 'Quando vocês abrem?', NULL, '2024-11-11 14:20:00+00', NULL),
    -- Chat 4: Pedro Oliveira (dbfd6c8a-41e3-4e95-b575-921983cea167)
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc075', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc075', '2024-11-11 16:30:00+00', 'dbfd6c8a-41e3-4e95-b575-921983cea167', 'Boa tarde! Vocês têm o produto X em estoque?', NULL, '2024-11-11 16:30:00+00', NULL),
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc076', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc076', '2024-11-11 16:35:00+00', 'dbfd6c8a-41e3-4e95-b575-921983cea167', 'Boa tarde, Pedro! Sim, temos disponível. Quantas unidades você precisa?', 'e8bf801b-d16a-4736-8df9-df9d9278293c', '2024-11-11 16:35:00+00', NULL),
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc077', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc077', '2024-11-11 16:37:00+00', 'dbfd6c8a-41e3-4e95-b575-921983cea167', 'Preciso de 5 unidades', NULL, '2024-11-11 16:37:00+00', NULL),
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc078', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc078', '2024-11-11 16:40:00+00', 'dbfd6c8a-41e3-4e95-b575-921983cea167', 'Temos sim! Vou separar para você. Pode retirar hoje ainda?', 'e8bf801b-d16a-4736-8df9-df9d9278293c', '2024-11-11 16:40:00+00', NULL),
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc079', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc079', '2024-11-11 16:45:00+00', 'dbfd6c8a-41e3-4e95-b575-921983cea167', 'Perfeito, vou aguardar', NULL, '2024-11-11 16:45:00+00', NULL),
    -- Chat 5: Julia Costa (948ed322-a961-46fd-b533-363103e94d3a)
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc080', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc080', '2024-11-12 11:40:00+00', '948ed322-a961-46fd-b533-363103e94d3a', 'Socorro!', NULL, '2024-11-12 11:40:00+00', NULL),
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc081', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc081', '2024-11-12 11:42:00+00', '948ed322-a961-46fd-b533-363103e94d3a', 'Preciso de ajuda urgente', NULL, '2024-11-12 11:42:00+00', NULL),
    ('e7fc687a-e0fa-49ea-af1b-7a2a2e6fc082', 'e7fc687a-e0fa-49ea-af1b-7a2a2e6fc082', '2024-11-12 11:45:00+00', '948ed322-a961-46fd-b533-363103e94d3a', 'Meu pedido não chegou e preciso dele hoje', NULL, '2024-11-12 11:45:00+00', NULL)
ON CONFLICT (id) DO NOTHING;

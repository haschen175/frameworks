-- ==========================================
-- Сервис сертификатов: структура базы данных
-- ==========================================

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    role TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    event_date TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    min_score REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    score REAL NOT NULL,
    passed INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (event_id) REFERENCES events (id)
);

CREATE TABLE IF NOT EXISTS certificates (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    result_id INTEGER NOT NULL,
    number TEXT NOT NULL,
    issued_at TEXT NOT NULL,
    is_revoked INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (event_id) REFERENCES events (id),
    FOREIGN KEY (result_id) REFERENCES results (id)
);

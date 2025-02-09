-- Database schema for Rat-Bot

-- Set WAL mode
PRAGMA journal_mode=WAL;

-- Create tables
CREATE TABLE rats (
    server_id TEXT NOT NULL,
    discord_user_id TEXT NOT NULL,
    count INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (server_id, discord_user_id)
);
DROP TRIGGER IF EXISTS update_rat_updated_at;

CREATE TRIGGER update_rat_updated_at
AFTER UPDATE ON rats
BEGIN
    UPDATE rats SET updated_at = CURRENT_TIMESTAMP WHERE server_id = NEW.server_id AND discord_user_id = NEW.discord_user_id;
END;
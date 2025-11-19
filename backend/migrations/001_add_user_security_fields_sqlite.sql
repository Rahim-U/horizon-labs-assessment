-- Migration: Add security and verification fields to users table (SQLite version)
-- Date: 2025-11-19
-- Description: Adds email verification, account locking, and security tracking fields to the users table
-- Note: SQLite doesn't support ALTER TABLE ADD COLUMN with NOT NULL and DEFAULT in older versions
-- This migration uses a workaround for SQLite compatibility

-- Add new columns to users table
-- SQLite requires DEFAULT values when adding NOT NULL columns
ALTER TABLE users ADD COLUMN is_verified INTEGER NOT NULL DEFAULT 0;
ALTER TABLE users ADD COLUMN is_active INTEGER NOT NULL DEFAULT 1;
ALTER TABLE users ADD COLUMN failed_login_attempts INTEGER NOT NULL DEFAULT 0;
ALTER TABLE users ADD COLUMN last_failed_login TEXT NULL;
ALTER TABLE users ADD COLUMN account_locked_until TEXT NULL;
ALTER TABLE users ADD COLUMN updated_at TEXT NOT NULL DEFAULT (datetime('now'));

-- Create indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_is_verified ON users(is_verified);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);

-- For existing users, set is_verified to TRUE (they are already in the system)
-- In production, you may want to set this to FALSE and require email verification
UPDATE users SET is_verified = 1 WHERE is_verified = 0;


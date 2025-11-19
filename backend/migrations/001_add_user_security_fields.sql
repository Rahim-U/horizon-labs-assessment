-- Migration: Add security and verification fields to users table
-- Date: 2025-11-19
-- Description: Adds email verification, account locking, and security tracking fields to the users table

-- Add new columns to users table
ALTER TABLE users ADD COLUMN is_verified BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE users ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT TRUE;
ALTER TABLE users ADD COLUMN failed_login_attempts INTEGER NOT NULL DEFAULT 0;
ALTER TABLE users ADD COLUMN last_failed_login TIMESTAMP WITH TIME ZONE NULL;
ALTER TABLE users ADD COLUMN account_locked_until TIMESTAMP WITH TIME ZONE NULL;
ALTER TABLE users ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- Create index on is_verified for faster lookups
CREATE INDEX idx_users_is_verified ON users(is_verified);

-- Create index on is_active for faster lookups
CREATE INDEX idx_users_is_active ON users(is_active);

-- For existing users, set is_verified to TRUE (they are already in the system)
-- In production, you may want to set this to FALSE and require email verification
UPDATE users SET is_verified = TRUE WHERE is_verified = FALSE;

-- Add comments for documentation
COMMENT ON COLUMN users.is_verified IS 'Whether the user has verified their email address';
COMMENT ON COLUMN users.is_active IS 'Whether the user account is active (not disabled)';
COMMENT ON COLUMN users.failed_login_attempts IS 'Number of consecutive failed login attempts';
COMMENT ON COLUMN users.last_failed_login IS 'Timestamp of the last failed login attempt';
COMMENT ON COLUMN users.account_locked_until IS 'Timestamp until which the account is locked (NULL if not locked)';
COMMENT ON COLUMN users.updated_at IS 'Timestamp of the last update to the user record';

-- Rollback script (save separately as rollback file):
-- ALTER TABLE users DROP COLUMN is_verified;
-- ALTER TABLE users DROP COLUMN is_active;
-- ALTER TABLE users DROP COLUMN failed_login_attempts;
-- ALTER TABLE users DROP COLUMN last_failed_login;
-- ALTER TABLE users DROP COLUMN account_locked_until;
-- ALTER TABLE users DROP COLUMN updated_at;
-- DROP INDEX IF EXISTS idx_users_is_verified;
-- DROP INDEX IF EXISTS idx_users_is_active;

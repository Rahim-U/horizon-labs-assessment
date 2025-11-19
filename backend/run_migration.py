"""
Script to apply database migrations for SQLite.
Run this script to update your database schema.
"""
import sqlite3
import os
from pathlib import Path

# Get the database path
db_path = Path(__file__).parent / "backend.db"
migration_path = Path(__file__).parent / "migrations" / "001_add_user_security_fields_sqlite.sql"

def run_migration():
    """Apply the migration to the SQLite database."""
    if not db_path.exists():
        print(f"Error: Database file not found at {db_path}")
        print("The database will be created automatically when you start the server.")
        return
    
    if not migration_path.exists():
        print(f"Error: Migration file not found at {migration_path}")
        return
    
    print(f"Connecting to database: {db_path}")
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # Read the migration file
        with open(migration_path, 'r', encoding='utf-8') as f:
            migration_sql = f.read()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        
        required_columns = [
            'is_verified', 'is_active', 'failed_login_attempts',
            'last_failed_login', 'account_locked_until', 'updated_at'
        ]
        
        missing_columns = [col for col in required_columns if col not in columns]
        
        if not missing_columns:
            print("✓ All required columns already exist. Migration not needed.")
            return
        
        print(f"Missing columns: {', '.join(missing_columns)}")
        print("Applying migration...")
        
        # Execute the migration
        # SQLite doesn't support multiple statements in execute(), so we split them
        statements = [s.strip() for s in migration_sql.split(';') if s.strip() and not s.strip().startswith('--')]
        
        for statement in statements:
            if statement:
                try:
                    cursor.execute(statement)
                    print(f"✓ Executed: {statement[:50]}...")
                except sqlite3.OperationalError as e:
                    # Ignore "duplicate column" errors
                    if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                        print(f"⚠ Skipped (already exists): {statement[:50]}...")
                    else:
                        raise
        
        conn.commit()
        print("\n✓ Migration completed successfully!")
        print(f"✓ Added columns: {', '.join(missing_columns)}")
        
    except Exception as e:
        conn.rollback()
        print(f"\n✗ Migration failed: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    run_migration()


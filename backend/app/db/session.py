from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
from ..core.config import settings

# Configure connection arguments based on database type
if settings.DATABASE_URL.startswith("sqlite"):
    # SQLite-specific configuration
    connect_args = {"check_same_thread": False}
    # Use StaticPool for SQLite to avoid connection issues
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args=connect_args,
        poolclass=StaticPool,
        echo=False,  # Set to True for SQL query logging in development
    )
else:
    # Production database configuration (PostgreSQL, MySQL, etc.)
    engine = create_engine(
        settings.DATABASE_URL,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_pre_ping=settings.DB_POOL_PRE_PING,
        echo=False,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Optional: Add connection event listeners for better error handling
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """Set SQLite pragmas for better performance and data integrity."""
    if settings.DATABASE_URL.startswith("sqlite"):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.close()
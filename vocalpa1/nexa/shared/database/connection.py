"""
Database connection and session management for Nexa
Supports SQLite for local development and PostgreSQL for production
"""

import os
from typing import Generator, Optional
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import logging

from .models import Base

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and sessions"""
    
    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or self._get_default_database_url()
        self.engine = self._create_engine()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def _get_default_database_url(self) -> str:
        """Get default database URL based on environment"""
        # Check for environment variable first
        if db_url := os.getenv("DATABASE_URL"):
            return db_url
            
        # Default to SQLite in the project directory
        db_path = os.path.join(os.path.dirname(__file__), "..", "..", "nexa.db")
        db_path = os.path.abspath(db_path)
        return f"sqlite:///{db_path}"
    
    def _create_engine(self) -> Engine:
        """Create SQLAlchemy engine with appropriate settings"""
        if self.database_url.startswith("sqlite"):
            # SQLite-specific settings
            engine = create_engine(
                self.database_url,
                poolclass=StaticPool,
                connect_args={
                    "check_same_thread": False,
                    "timeout": 20
                },
                echo=os.getenv("DEBUG_SQL", "false").lower() == "true"
            )
            
            # Enable foreign key constraints for SQLite
            @event.listens_for(engine, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.execute("PRAGMA synchronous=NORMAL")
                cursor.execute("PRAGMA cache_size=10000")
                cursor.execute("PRAGMA temp_store=MEMORY")
                cursor.close()
                
        else:
            # PostgreSQL or other database settings
            engine = create_engine(
                self.database_url,
                pool_pre_ping=True,
                pool_recycle=300,
                echo=os.getenv("DEBUG_SQL", "false").lower() == "true"
            )
            
        return engine
    
    def create_tables(self):
        """Create all database tables"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            raise
    
    def drop_tables(self):
        """Drop all database tables (use with caution!)"""
        try:
            Base.metadata.drop_all(bind=self.engine)
            logger.info("Database tables dropped successfully")
        except Exception as e:
            logger.error(f"Failed to drop database tables: {e}")
            raise
    
    def get_session(self) -> Generator[Session, None, None]:
        """Get database session with automatic cleanup"""
        session = self.SessionLocal()
        try:
            yield session
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    def get_session_sync(self) -> Session:
        """Get synchronous database session (manual cleanup required)"""
        return self.SessionLocal()
    
    def health_check(self) -> bool:
        """Check database connectivity"""
        try:
            with self.get_session() as session:
                session.execute("SELECT 1")
                return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False


# Global database manager instance
db_manager: Optional[DatabaseManager] = None


def init_database(database_url: Optional[str] = None) -> DatabaseManager:
    """Initialize global database manager"""
    global db_manager
    db_manager = DatabaseManager(database_url)
    db_manager.create_tables()
    return db_manager


def get_database() -> DatabaseManager:
    """Get global database manager instance"""
    if db_manager is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    return db_manager


def get_db_session() -> Generator[Session, None, None]:
    """FastAPI dependency for database sessions"""
    db = get_database()
    yield from db.get_session()


# Migration utilities
class MigrationManager:
    """Handle database schema migrations"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_current_version(self) -> int:
        """Get current database schema version"""
        try:
            with self.db_manager.get_session() as session:
                result = session.execute(
                    "SELECT version FROM schema_version ORDER BY applied_at DESC LIMIT 1"
                )
                row = result.fetchone()
                return row[0] if row else 0
        except:
            # Table doesn't exist, assume version 0
            return 0
    
    def apply_migration(self, version: int, sql: str):
        """Apply a database migration"""
        with self.db_manager.get_session() as session:
            try:
                # Execute migration SQL
                session.execute(sql)
                
                # Record migration
                session.execute(
                    "INSERT INTO schema_version (version, applied_at) VALUES (?, ?)",
                    (version, "datetime('now')")
                )
                session.commit()
                logger.info(f"Applied migration version {version}")
            except Exception as e:
                session.rollback()
                logger.error(f"Failed to apply migration {version}: {e}")
                raise
    
    def create_migration_table(self):
        """Create schema version tracking table"""
        with self.db_manager.get_session() as session:
            session.execute("""
                CREATE TABLE IF NOT EXISTS schema_version (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    version INTEGER NOT NULL,
                    applied_at DATETIME NOT NULL
                )
            """)
            session.commit()


# Utility functions for common database operations
def ensure_user_exists(session: Session, user_id: str) -> int:
    """Ensure user exists in database, create if not found"""
    from .models import User
    
    user = session.query(User).filter(User.user_id == user_id).first()
    if not user:
        user = User(user_id=user_id, is_logged_in=True)
        session.add(user)
        session.commit()
        session.refresh(user)
    
    return user.id


def get_user_preference(session: Session, user_id: str, key: str, default=None):
    """Get user preference value"""
    from .models import User, UserPreference
    
    user = session.query(User).filter(User.user_id == user_id).first()
    if not user:
        return default
    
    pref = session.query(UserPreference).filter(
        UserPreference.user_id == user.id,
        UserPreference.key == key
    ).first()
    
    if not pref:
        return default
    
    # Parse value based on type
    if pref.value_type == "boolean":
        return pref.value.lower() == "true"
    elif pref.value_type == "number":
        return float(pref.value) if "." in pref.value else int(pref.value)
    elif pref.value_type == "json":
        import json
        return json.loads(pref.value)
    else:
        return pref.value


def set_user_preference(session: Session, user_id: str, key: str, value, value_type: str = None):
    """Set user preference value"""
    from .models import User, UserPreference
    import json
    
    user_pk = ensure_user_exists(session, user_id)
    
    # Determine value type if not specified
    if value_type is None:
        if isinstance(value, bool):
            value_type = "boolean"
        elif isinstance(value, (int, float)):
            value_type = "number"
        elif isinstance(value, (dict, list)):
            value_type = "json"
        else:
            value_type = "string"
    
    # Convert value to string
    if value_type == "json":
        value_str = json.dumps(value)
    else:
        value_str = str(value)
    
    # Update or create preference
    pref = session.query(UserPreference).filter(
        UserPreference.user_id == user_pk,
        UserPreference.key == key
    ).first()
    
    if pref:
        pref.value = value_str
        pref.value_type = value_type
    else:
        pref = UserPreference(
            user_id=user_pk,
            key=key,
            value=value_str,
            value_type=value_type
        )
        session.add(pref)
    
    session.commit()

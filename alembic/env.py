"""
Alembic Environment Configuration
"""
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from sqlalchemy.engine import URL
from alembic import context
import os
import sys
from typing import Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.core.config import settings
from app.db.base import Base
from app.models import user, audit, address, branchlocation  # Import all models

# Alembic Config object
config = context.config

# Set database URL from environment
database_url: str = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
config.set_main_option("sqlalchemy.url", database_url)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata for autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.
    
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url: Optional[str] = config.get_main_option("sqlalchemy.url")
    
    if url is None:
        raise ValueError(
            "Database URL not found in alembic configuration. "
            "Please ensure DATABASE_URL is set in your .env file."
        )
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    # Get the database URL with proper type
    url: Optional[str] = config.get_main_option("sqlalchemy.url")
    
    # Ensure URL is not None
    if url is None:
        raise ValueError(
            "Database URL not found in alembic configuration. "
            "Please ensure DATABASE_URL is set in your .env file."
        )
    
    # Create engine with NullPool for Alembic
    # Type ignore is added for poolclass parameter due to SQLAlchemy typing quirks
    connectable = create_engine(
        url,
        poolclass=pool.NullPool,  # type: ignore[arg-type]
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
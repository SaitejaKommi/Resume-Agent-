from logging.config import fileConfig

from sqlalchemy import engine_from_config, create_engine
from sqlalchemy import pool
from sqlalchemy.engine import make_url

from alembic import context

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Load .env from repo root or backend directory
repo_root = Path(__file__).resolve().parents[3]
backend_root = Path(__file__).resolve().parents[2]
env_file = repo_root / ".env"
if not env_file.exists():
    env_file = backend_root / ".env"
if env_file.exists():
    load_dotenv(env_file)

# add the app directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.base import Base  # noqa: E402

# Get DATABASE_URL from environment
database_url_str = os.getenv('DATABASE_URL', 'postgresql+asyncpg://resumeagent:resumeagent@localhost:5432/resumeagent')
database_url = make_url(database_url_str)
if database_url.drivername.endswith("+asyncpg"):
    database_url = database_url.set(drivername=database_url.drivername.replace("+asyncpg", "+psycopg2"))

config.set_main_option('sqlalchemy.url', str(database_url))

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # Use the database_url we converted from asyncpg to psycopg2
    # Extract connection parameters
    url = database_url
    kwargs = {
        'host': url.host or '127.0.0.1',
        'port': url.port or 5432,
        'user': url.username or 'resumeagent', 
        'password': url.password or 'resumeagent',
        'database': url.database or 'resumeagent',
    }
    
    connectable = create_engine(
        f"postgresql+psycopg2://{kwargs['user']}:{kwargs['password']}@{kwargs['host']}:{kwargs['port']}/{kwargs['database']}",
        poolclass=pool.NullPool
    )
    
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

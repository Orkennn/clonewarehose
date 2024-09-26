from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy import create_engine  # For synchronous migration engine
from alembic import context

# Import your models' Base
from core.models import Base  # Adjust this to the correct import path
from core.settings import settings  # Import your settings

config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Set up the target metadata from your models
target_metadata = Base.metadata

# Update `sqlalchemy.url` in config dynamically using your `settings.db_url_sync`
config.set_main_option('sqlalchemy.url', settings.db_url_sync)


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = create_engine(
        config.get_main_option("sqlalchemy.url")
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

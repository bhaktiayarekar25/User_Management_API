from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context


# Import your models and Base
from database import Base
from models import User

# Target metadata for Alembic autogenerate
target_metadata = Base.metadata

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

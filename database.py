from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database

# PostgreSQL connection URL
DATABASE_URL = "postgresql+asyncpg://fastapi_user:fastapi_pass@localhost:5432/user_management"
# DATABASE_URL = "postgresql+asyncpg://bhaktiayarekar@localhost:5432/postgres"

# SQLAlchemy setup
Base = declarative_base()
metadata = Base.metadata

engine = create_engine(DATABASE_URL.replace("+asyncpg", ""))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Databases (async)
database = Database(DATABASE_URL)

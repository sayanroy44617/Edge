import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utils.utils import get_settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

settings = get_settings()

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_db_and_tables():
    try:
        Base.metadata.create_all(engine)
        logger.info("Database and tables created successfully.")
    except Exception as e:
        logger.error(f"❌ Critical Error: Failed to create tables. Database might be unavailable. Error: {e}")
        raise e

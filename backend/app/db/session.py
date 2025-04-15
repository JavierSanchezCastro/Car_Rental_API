from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.Settings import settings

SQLALCHEMY_DATABASE_URL = settings.DB_URL.unicode_string()

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)


SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)


def get_session() -> Generator:
    try:
        db = SessionLocal()
        yield db
    except Exception as e:
        print(f"Rolling Back [{e}]")
        db.rollback()
        raise
    finally:
        print("Closing Session")
        db.close()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sqlite_file_name = "blog.db"

SQLALCHEMY_DATABASE_URL = 'sqlite:///./blog.db'

CONNECT_ARGS = {"check_same_thread": False}

engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args=CONNECT_ARGS)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

Base = declarative_base()

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from typing import Annotated

# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import sessionmaker
import sqlite3
from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session
from . import models
from dotenv import load_dotenv
from .utils import create_file_and_directories_if_not_exist
import os

# Load .env jika menggunakan variabel environment
load_dotenv()

DEFAULT_DB_URL = "sqlite:///app/data/db.sqlite"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB_URL)

if DATABASE_URL == DEFAULT_DB_URL:
    print("Using default database URL")
    db_path = os.path.join(os.path.dirname(__file__), "data", "db.sqlite")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path) 
    conn.close()

# Koneksi ke database
connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

# Dependency untuk mendapatkan sesi database
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# Fungsi untuk test koneksi: python -c "from app.database import test_connection; print(test_connection())"
# def test_connection():
#     try:
#         with engine.connect() as connection:
#             result = connection.execute(text("SELECT 1"))
#             return f"Database Connected: {result.scalar()}"
#     except Exception as e:
#         raise Exception(f"Database Connection Failed: {str(e)}")

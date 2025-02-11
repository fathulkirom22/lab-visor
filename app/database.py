from typing import Annotated

import sqlite3
from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session, text
from . import models
from dotenv import load_dotenv
import os

# Load .env jika menggunakan variabel environment
load_dotenv()

DEFAULT_DB_URL = "sqlite:///app/data/db.sqlite"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB_URL)

connect_args = {}
if DATABASE_URL == DEFAULT_DB_URL:
    print("\t[INFO] Using default database")
    connect_args = {"check_same_thread": False}
    db_path = os.path.join(os.path.dirname(__file__), "data", "db.sqlite")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path) 
    conn.close()

# Koneksi ke database
engine = create_engine(DATABASE_URL, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# Fungsi untuk test koneksi: python -c "from app.database import test_connection; print(test_connection())"
def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return f"Database Connected: {result.scalar()}"
    except Exception as e:
        raise Exception(f"Database Connection Failed: {str(e)}")

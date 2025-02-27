"""Module providing a function connect to db."""

import os
import sqlite3

from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session, text
from dotenv import load_dotenv

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
    """create db and table from model"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """get db session"""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def test_connection():
    """test db connection"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return f"Database Connected: {result.scalar()}"
    except Exception as e:
        raise ConnectionError(f"Database Connection Failed: {str(e)}") from e

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load .env jika menggunakan variabel environment
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Koneksi ke database
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency untuk mendapatkan sesi database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fungsi untuk test koneksi: python -c "from app.database import test_connection; print(test_connection())"
def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return f"Database Connected: {result.scalar()}"
    except Exception as e:
        raise Exception(f"Database Connection Failed: {str(e)}")

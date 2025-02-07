import datetime
from fastapi import FastAPI
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from .database import create_db_and_tables, SessionDep, get_session, engine
from .models import SysDataTracker
from sqlmodel import Session, select, func, text
import psutil

interval = 900

def printit():
    with Session(engine) as session:
        # Simpan data ke database
        cpu_percent = psutil.cpu_percent(interval=interval) 
        memory_percent = psutil.virtual_memory().percent
        data = SysDataTracker(cpu=cpu_percent, memory=memory_percent)
        session.add(data)
        session.commit()
        session.refresh(data)

        # Hapus data jika melebihi batas
        nama_tabel = "sysdatatracker"  # Contoh
        kolom_timestamp = "created_at"  # Contoh
        limit = 1000
        row = session.exec(select(func.count()).select_from(SysDataTracker)).one()
        if row > limit:
            count_delete = row - limit
            query_delete = text(f"DELETE FROM {nama_tabel} ORDER BY {kolom_timestamp} ASC LIMIT {count_delete}")
            session.exec(query_delete)  # Nilai parameter sebagai tuple
            session.commit()

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_tables()
    scheduler = BackgroundScheduler()
    scheduler.add_job(printit,"interval",seconds=interval)
    scheduler.start()
    yield
    scheduler.shutdown()
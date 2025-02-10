import datetime
from fastapi import FastAPI
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from .database import create_db_and_tables, SessionDep, get_session, engine
from .models import SysDataTracker
from sqlmodel import Session, select, func, text
import psutil

interval = 900

def track_resource_usage():
    with Session(engine) as session:
        # Save new data
        cpu_percent = psutil.cpu_percent(interval=1) 
        memory_percent = psutil.virtual_memory().percent
        data = SysDataTracker(cpu=cpu_percent, memory=memory_percent)
        session.add(data)
        session.commit()
        session.refresh(data)

        # Delete old data
        table_name = "sysdatatracker"
        timestamp_column = "created_at"
        limit = 1000
        row = session.exec(select(func.count()).select_from(SysDataTracker)).one()
        if row > limit:
            count_delete = row - limit
            query_delete = text(f"DELETE FROM {table_name} ORDER BY {timestamp_column} ASC LIMIT {count_delete}")
            session.exec(query_delete)
            session.commit()

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_tables()
    scheduler = BackgroundScheduler()
    scheduler.add_job(track_resource_usage,"interval", seconds=interval, misfire_grace_time=5, coalesce=True)
    scheduler.start()
    yield
    scheduler.shutdown()
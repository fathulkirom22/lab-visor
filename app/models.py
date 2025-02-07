# from sqlalchemy.ext.automap import automap_base
# from .database import engine
from sqlmodel import Field, SQLModel
from datetime import datetime

# Base = automap_base()
# Base.prepare(engine, reflect=True)

class SysDataTracker(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cpu: float
    memory: float
    created_at: datetime = Field(default=datetime.now())

# Ambil model yang sudah ada
# SysDataTracker = Base.classes.sys_data_tracker  # Pastikan nama tabel sesuai dengan database

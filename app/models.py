from sqlmodel import Field, SQLModel
from datetime import datetime

class SysDataTracker(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cpu: float
    memory: float
    created_at: datetime = Field(default_factory=lambda: datetime.now())

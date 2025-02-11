from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from pydantic import HttpUrl
from datetime import datetime
from .utils import camel_to_snake

class BaseModel(SQLModel):
    __abstract__ = True  # Make it an abstract base class
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime = Field(default_factory=lambda: datetime.now())
    deleted_at: Optional[datetime] = Field(default=None)
    
class SysDataTracker(BaseModel, table=True):
    __tablename__ = "sys_data_tracker"
    cpu: float
    memory: float

class CategoryApp(BaseModel, table=True):
    __tablename__ = "category_app"
    name: str
    icon: Optional[str] = Field(default=None)
    apps: Optional[list["ShortcutApp"]] = Relationship(back_populates="category_app")

class ShortcutApp(BaseModel, table=True):
    __tablename__ = "shortcut_app"
    name: str
    link: str
    icon: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    category_app_id: Optional[int] = Field(default=None, foreign_key="category_app.id")
    category_app: Optional[CategoryApp] = Relationship(back_populates="apps")

    @classmethod
    def validate(cls, **data):
        validated_data = HttpUrl.validate(data["link"])
        data["link"] = str(validated_data)
        return cls(**data)

"""module for model on db"""
from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from pydantic import HttpUrl

class BaseModel(SQLModel):
    """base model for all model"""
    __abstract__ = True  # Make it an abstract base class
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime = Field(default_factory=lambda: datetime.now())
    deleted_at: Optional[datetime] = Field(default=None)

class SysDataTracker(BaseModel, table=True):
    """model for table sys_data_tracker"""
    __tablename__ = "sys_data_tracker"
    cpu: float
    memory: float

class CategoryApp(BaseModel, table=True):
    """model for table category_app"""
    __tablename__ = "category_app"
    name: str
    icon: Optional[str] = Field(default=None)
    theme: str = Field(default='primary')
    order: int = Field(default=99)
    apps: Optional[list["ShortcutApp"]] = Relationship(back_populates="category_app")

class ShortcutApp(BaseModel, table=True):
    """model for table shortcut_app"""
    __tablename__ = "shortcut_app"
    name: str
    link: str
    icon: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    category_app_id: Optional[int] = Field(default=None, foreign_key="category_app.id")
    category_app: Optional[CategoryApp] = Relationship(back_populates="apps")

    @classmethod
    def validate(cls, value):
        validated_data = HttpUrl(value["link"])
        value["link"] = str(validated_data)
        return cls(**value)

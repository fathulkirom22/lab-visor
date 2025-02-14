"""module for models payload & form request"""
from typing import Optional

from pydantic import BaseModel

class ShortcutAppCreate(BaseModel):
    """model for create shortcut app"""
    id: Optional[int] = None
    name: str
    link: str
    icon: Optional[str] = None
    description: Optional[str] = None
    category_app_id: Optional[int] = None

class CategoryAppCreate(BaseModel):
    """model for create category app"""
    id: Optional[int] = None
    name: str
    icon: Optional[str] = None

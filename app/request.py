from typing import Optional

from pydantic import BaseModel, HttpUrl

class ShortcutAppCreate(BaseModel):
    id: Optional[int] = None
    name: str
    link: str
    icon: Optional[str] = None
    description: Optional[str] = None
    category_app_id: Optional[int] = None

class CategoryAppCreate(BaseModel):
    id: Optional[int] = None
    name: str
    icon: Optional[str] = None

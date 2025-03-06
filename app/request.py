"""module for models payload & form request"""

from typing import Optional, Annotated

from pydantic import BaseModel, Field, HttpUrl, ValidationError, field_validator


class ShortcutAppCreate(BaseModel):
    """model for create shortcut app"""

    id: Annotated[Optional[int], Field(...)] = None
    name: Annotated[str, Field(..., min_length=3, max_length=50)]
    link: Annotated[str, Field(..., min_length=10, max_length=255)]
    icon: Annotated[Optional[str], Field(...)] = None
    description: Annotated[Optional[str], Field(...)] = None
    category_app_id: Annotated[Optional[int], Field(...)] = None
    container_name: Annotated[Optional[str], Field(...)] = None

    @field_validator("link")
    @classmethod
    def validate_link(cls, value: str) -> str:
        try:
            return str(HttpUrl(value))
        except ValidationError:
            raise ValueError("Invalid URL format")


class CategoryAppCreate(BaseModel):
    """model for create category app"""

    id: Annotated[Optional[int], Field(...)] = None
    name: Annotated[str, Field(..., min_length=3, max_length=50)]
    icon: Annotated[Optional[str], Field(...)] = None
    theme: Annotated[str, Field(...)] = "primary"
    order: Annotated[int, Field(..., ge=1, le=99)] = 99

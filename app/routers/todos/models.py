from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models import optional

from .enums import Status


class Todo(BaseModel):
    title: str = Field(max_length=128, description="Todo title")
    description: Optional[str] = Field(
        None, max_length=1300, description="Todo details"
    )
    completed: Optional[bool] = False


@optional
class TodoUpdate(Todo):
    pass


class TodoRecord(Todo):
    id: str
    owner: str
    created_date: datetime
    updated_date: datetime


class ResponseStatus(BaseModel):
    status: Status

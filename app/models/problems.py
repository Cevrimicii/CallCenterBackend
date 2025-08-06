from sqlmodel import SQLModel, Field
from typing import Optional

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Problem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    location: str
    problem: str
    estimated_completion_time: datetime

from sqlmodel import Column, SQLModel, Field, JSON, Relationship
from typing import List, Optional,Dict

from sqlmodel import Column, SQLModel, Field, JSON, Relationship
from typing import Optional, Dict
from datetime import datetime

from app.models.invoice import Invoice
from app.models.user import User

class AgentIntentLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    intent: str  # örn: "ek_hizmet_talebi", "paket_degistirme", "taahhüt_sorgulama"
    message: str
    created_at: datetime = Field(default_factory=datetime.now)

    user: Optional[User] = Relationship()
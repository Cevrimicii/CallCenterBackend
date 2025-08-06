from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.user import User

class AgentIntentLog(SQLModel, table=True):
    __tablename__ = "agent_intent_log"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)
    intent: str = Field(max_length=100)  # örn: "ek_hizmet_talebi", "paket_degistirme"
    message: str = Field(max_length=2000)
    confidence: Optional[float] = Field(default=None, ge=0, le=1)  # AI confidence score
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # İlişkiler
    user: Optional["User"] = Relationship()
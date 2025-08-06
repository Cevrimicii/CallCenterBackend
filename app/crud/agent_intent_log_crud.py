from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from app.models.agentintentlog import AgentIntentLog
from app.db.database import engine


def get_agent_intent_logs() -> List[AgentIntentLog]:
    """Tüm agent intent loglarını getir"""
    with Session(engine) as session:
        return session.exec(select(AgentIntentLog)).all()


def get_agent_intent_log_by_id(log_id: int) -> Optional[AgentIntentLog]:
    """ID'ye göre agent intent log getir"""
    with Session(engine) as session:
        return session.get(AgentIntentLog, log_id)


def get_agent_intent_logs_by_user(user_id: int) -> List[AgentIntentLog]:
    """Kullanıcıya göre agent intent loglarını getir"""
    with Session(engine) as session:
        query = select(AgentIntentLog).where(AgentIntentLog.user_id == user_id)
        return session.exec(query).all()


def get_agent_intent_logs_by_intent(intent: str) -> List[AgentIntentLog]:
    """Intent'e göre logları getir"""
    with Session(engine) as session:
        query = select(AgentIntentLog).where(AgentIntentLog.intent == intent)
        return session.exec(query).all()


def get_agent_intent_logs_by_date_range(start_date: datetime, end_date: datetime) -> List[AgentIntentLog]:
    """Belirli bir tarih aralığındaki logları getir"""
    with Session(engine) as session:
        query = select(AgentIntentLog).where(
            AgentIntentLog.created_at >= start_date,
            AgentIntentLog.created_at <= end_date
        )
        return session.exec(query).all()


def create_agent_intent_log(agent_intent_log: AgentIntentLog) -> AgentIntentLog:
    """Yeni agent intent log oluştur"""
    with Session(engine) as session:
        session.add(agent_intent_log)
        session.commit()
        session.refresh(agent_intent_log)
        return agent_intent_log


def update_agent_intent_log(log_id: int, log_data: dict) -> Optional[AgentIntentLog]:
    """Agent intent log bilgilerini güncelle"""
    with Session(engine) as session:
        agent_intent_log = session.get(AgentIntentLog, log_id)
        if agent_intent_log:
            for key, value in log_data.items():
                setattr(agent_intent_log, key, value)
            session.add(agent_intent_log)
            session.commit()
            session.refresh(agent_intent_log)
            return agent_intent_log
        return None


def delete_agent_intent_log(log_id: int) -> bool:
    """Agent intent log sil"""
    with Session(engine) as session:
        agent_intent_log = session.get(AgentIntentLog, log_id)
        if agent_intent_log:
            session.delete(agent_intent_log)
            session.commit()
            return True
        return False


def get_recent_agent_intent_logs(limit: int = 50) -> List[AgentIntentLog]:
    """En son logları getir"""
    with Session(engine) as session:
        query = select(AgentIntentLog).order_by(AgentIntentLog.created_at.desc()).limit(limit)
        return session.exec(query).all()


def get_agent_intent_logs_by_user_and_intent(user_id: int, intent: str) -> List[AgentIntentLog]:
    """Kullanıcı ve intent'e göre logları getir"""
    with Session(engine) as session:
        query = select(AgentIntentLog).where(
            AgentIntentLog.user_id == user_id,
            AgentIntentLog.intent == intent
        )
        return session.exec(query).all()

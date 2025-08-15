from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from app.models.agentintentlog import AgentIntentLog
from app.db.database import engine
from app.utils.logging_config import get_logger, log_database_operation, log_error

logger = get_logger('app.crud.agent_intent_log')


def get_agent_intent_logs() -> List[AgentIntentLog]:
    """Tüm agent intent loglarını getir"""
    try:
        logger.info("Fetching all agent intent logs")
        with Session(engine) as session:
            result = session.exec(select(AgentIntentLog)).all()
            log_database_operation("SELECT", "agent_intent_logs", details=f"Retrieved {len(result)} records")
            return result
    except Exception as e:
        log_error(e, "Error fetching all agent intent logs")
        raise


def get_agent_intent_log_by_id(log_id: int) -> Optional[AgentIntentLog]:
    """ID'ye göre agent intent log getir"""
    try:
        logger.info(f"Fetching agent intent log by ID: {log_id}")
        with Session(engine) as session:
            result = session.get(AgentIntentLog, log_id)
            if result:
                log_database_operation("SELECT", "agent_intent_logs", record_id=log_id, details="Record found")
            else:
                logger.warning(f"Agent intent log not found with ID: {log_id}")
            return result
    except Exception as e:
        log_error(e, f"Error fetching agent intent log by ID: {log_id}")
        raise


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
    try:
        logger.info(f"Creating new agent intent log for user: {agent_intent_log.user_id}, intent: {agent_intent_log.intent}")
        with Session(engine) as session:
            session.add(agent_intent_log)
            session.commit()
            session.refresh(agent_intent_log)
            log_database_operation("INSERT", "agent_intent_logs", record_id=agent_intent_log.id, 
                                 details=f"User: {agent_intent_log.user_id}, Intent: {agent_intent_log.intent}")
            logger.info(f"Successfully created agent intent log with ID: {agent_intent_log.id}")
            return agent_intent_log
    except Exception as e:
        log_error(e, f"Error creating agent intent log for user: {agent_intent_log.user_id}")
        raise


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
    try:
        logger.info(f"Deleting agent intent log with ID: {log_id}")
        with Session(engine) as session:
            agent_intent_log = session.get(AgentIntentLog, log_id)
            if agent_intent_log:
                session.delete(agent_intent_log)
                session.commit()
                log_database_operation("DELETE", "agent_intent_logs", record_id=log_id, details="Successfully deleted")
                logger.info(f"Successfully deleted agent intent log with ID: {log_id}")
                return True
            else:
                logger.warning(f"Attempted to delete non-existent agent intent log with ID: {log_id}")
                return False
    except Exception as e:
        log_error(e, f"Error deleting agent intent log with ID: {log_id}")
        raise


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

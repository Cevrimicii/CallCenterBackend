from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from app.crud.agent_intent_log_crud import (
    get_agent_intent_logs,
    get_agent_intent_log_by_id,
    get_agent_intent_logs_by_user,
    get_agent_intent_logs_by_intent,
    get_agent_intent_logs_by_date_range,
    create_agent_intent_log,
    update_agent_intent_log,
    delete_agent_intent_log,
    get_recent_agent_intent_logs,
    get_agent_intent_logs_by_user_and_intent
)
from app.models.agentintentlog import AgentIntentLog

router = APIRouter(
    prefix="/agent-logs",
    tags=["agent-logs"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[AgentIntentLog])
def get_all_agent_intent_logs():
    """Tüm agent intent loglarını getir"""
    return get_agent_intent_logs()

@router.get("/{log_id}", response_model=AgentIntentLog)
def get_agent_intent_log(log_id: int):
    """ID'ye göre agent intent log getir"""
    log = get_agent_intent_log_by_id(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Agent intent log not found")
    return log

@router.get("/user/{user_id}", response_model=List[AgentIntentLog])
def get_user_agent_intent_logs(user_id: int):
    """Kullanıcının agent intent loglarını getir"""
    return get_agent_intent_logs_by_user(user_id)

@router.get("/intent/{intent}", response_model=List[AgentIntentLog])
def get_logs_by_intent(intent: str):
    """Intent'e göre logları getir"""
    return get_agent_intent_logs_by_intent(intent)

@router.get("/recent/{limit}")
def get_recent_logs(limit: int = 50):
    """En son logları getir"""
    return get_recent_agent_intent_logs(limit)

@router.post("/", response_model=AgentIntentLog)
def create_new_agent_intent_log(agent_intent_log: AgentIntentLog):
    """Yeni agent intent log oluştur"""
    return create_agent_intent_log(agent_intent_log)

@router.put("/{log_id}", response_model=AgentIntentLog)
def update_agent_intent_log_info(log_id: int, log_data: dict):
    """Agent intent log bilgilerini güncelle"""
    log = update_agent_intent_log(log_id, log_data)
    if not log:
        raise HTTPException(status_code=404, detail="Agent intent log not found")
    return log

@router.delete("/{log_id}")
def delete_agent_intent_log_by_id(log_id: int):
    """Agent intent log sil"""
    success = delete_agent_intent_log(log_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent intent log not found")
    return {"message": "Agent intent log deleted successfully"}

@router.get("/date-range/{start_date}/{end_date}", response_model=List[AgentIntentLog])
def get_logs_by_date_range(start_date: datetime, end_date: datetime):
    """Belirli bir tarih aralığındaki logları getir"""
    return get_agent_intent_logs_by_date_range(start_date, end_date)

@router.get("/user/{user_id}/intent/{intent}", response_model=List[AgentIntentLog])
def get_user_logs_by_intent(user_id: int, intent: str):
    """Kullanıcı ve intent'e göre logları getir"""
    return get_agent_intent_logs_by_user_and_intent(user_id, intent)

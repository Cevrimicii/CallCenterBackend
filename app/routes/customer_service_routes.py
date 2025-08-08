from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime, timedelta
from sqlmodel import Session, select
from app.db.database import engine
from app.models.user import User
from app.models.subscription import Subscription
from app.models.invoice import Invoice
from app.models.problems import Problem
from app.models.agentintentlog import AgentIntentLog
from app.crud.user_crud import get_user_by_phone
from app.crud.subscription_crud import get_user_active_subscription
from app.crud.invoice_crud import get_invoices_by_user
from app.crud.remaining_uses_crud import get_remaining_uses_by_user
from app.crud.agent_intent_log_crud import create_agent_intent_log

router = APIRouter(
    prefix="/customer-service",
    tags=["customer-service"],
    responses={404: {"description": "Not found"}},
)

@router.get("/customer/{phone_number}")
def get_customer_info(phone_number: str):
    """Telefon numarasına göre müşteri bilgilerini getir (çağrı merkezi için)"""
    user = get_user_by_phone(phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Aktif abonelik
    active_subscription = get_user_active_subscription(user.id)
    
    # Son 5 fatura
    recent_invoices = get_invoices_by_user(user.id)[:5]
    
    # Kalan kullanımlar
    remaining_uses = get_remaining_uses_by_user(user.id)
    
    return {
        "customer": {
            "id": user.id,
            "name": f"{user.name} {user.surname}",
            "phone": user.phone_number,
            "email": user.email,
            "is_active": user.is_active,
            "created_at": user.created_at
        },
        "subscription": {
            "id": active_subscription.id if active_subscription else None,
            "package_id": active_subscription.package_id if active_subscription else None,
            "start_date": active_subscription.start_date if active_subscription else None,
            "end_date": active_subscription.end_date if active_subscription else None,
            "contract_months": active_subscription.contract_months if active_subscription else None,
            "is_active": active_subscription.is_active if active_subscription else False
        } if active_subscription else None,
        "recent_invoices": [
            {
                "id": inv.id,
                "invoice_number": inv.invoice_number,
                "total_amount": inv.total_amount,
                "status": inv.status,
                "due_date": inv.due_date,
                "created_at": inv.created_at
            }
            for inv in recent_invoices
        ],
        "remaining_uses": [
            {
                "service_type": ru.service_type,
                "remaining_count": ru.remaining_count,
                "total_allocated": ru.total_allocated,
                "expires_at": ru.expires_at
            }
            for ru in remaining_uses
        ]
    }

@router.post("/log-interaction")
def log_customer_interaction(user_id: Optional[int], phone_number: Optional[str], intent: str, message: str, confidence: Optional[float] = None):
    """Müşteri etkileşimini logla"""
    if not user_id and phone_number:
        user = get_user_by_phone(phone_number)
        user_id = user.id if user else None
    
    log = AgentIntentLog(
        user_id=user_id,
        intent=intent,
        message=message,
        confidence=confidence,
        created_at=datetime.utcnow()
    )
    
    return create_agent_intent_log(log)

@router.get("/quick-search/{search_term}")
def quick_customer_search(search_term: str):
    """Hızlı müşteri arama (telefon, isim veya email ile)"""
    with Session(engine) as session:
        # Telefon numarası ile arama
        phone_results = session.exec(
            select(User).where(User.phone_number.contains(search_term))
        ).all()
        
        # İsim ile arama
        name_results = session.exec(
            select(User).where(
                User.name.contains(search_term) | 
                User.surname.contains(search_term)
            )
        ).all()
        
        # Email ile arama
        email_results = session.exec(
            select(User).where(User.email.contains(search_term))
        ).all() if search_term and "@" in search_term else []
        
        # Sonuçları birleştir ve tekrarları kaldır
        all_results = list({user.id: user for user in phone_results + name_results + email_results}.values())
        
        return {
            "results": [
                {
                    "id": user.id,
                    "name": f"{user.name} {user.surname}",
                    "phone": user.phone_number,
                    "email": user.email,
                    "is_active": user.is_active
                }
                for user in all_results[:10]  # İlk 10 sonuç
            ],
            "total_found": len(all_results)
        }

@router.get("/customer/{user_id}/problems")
def get_customer_problems(user_id: int):
    """Müşterinin bildirdiği problemleri getir"""
    with Session(engine) as session:
        # Müşterinin bulunduğu lokasyondaki problemler (basit implementasyon)
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        # Tüm aktif problemleri getir (gerçek uygulamada lokasyon bazlı filtreleme yapılabilir)
        problems = session.exec(
            select(Problem).where(Problem.status != "completed")
        ).all()
        
        return {
            "customer_id": user_id,
            "problems": [
                {
                    "id": p.id,
                    "location": p.location,
                    "problem": p.problem,
                    "status": p.status,
                    "priority": p.priority,
                    "estimated_completion_time": p.estimated_completion_time,
                    "created_at": p.created_at
                }
                for p in problems
            ]
        }

@router.post("/customer/{user_id}/complaint")
def create_customer_complaint(user_id: int, complaint: str, priority: str = "medium"):
    """Müşteri şikayeti oluştur"""
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        problem = Problem(
            location=f"Customer Complaint - {user.phone_number}",
            problem=complaint,
            status="pending",
            priority=priority,
            estimated_completion_time=datetime.utcnow() + timedelta(days=3),  # 3 gün içinde çözülmesi hedefi
            created_at=datetime.utcnow()
        )
        
        session.add(problem)
        session.commit()
        session.refresh(problem)
        
        # Şikayeti logla
        log = AgentIntentLog(
            user_id=user_id,
            intent="complaint",
            message=f"Customer complaint created: {complaint[:100]}...",
            created_at=datetime.utcnow()
        )
        session.add(log)
        session.commit()
        
        return {
            "message": "Complaint created successfully",
            "complaint_id": problem.id,
            "estimated_resolution": problem.estimated_completion_time
        }

@router.get("/customer/{user_id}/interaction-history")
def get_customer_interaction_history(user_id: int, limit: int = 20):
    """Müşterinin etkileşim geçmişini getir"""
    with Session(engine) as session:
        interactions = session.exec(
            select(AgentIntentLog)
            .where(AgentIntentLog.user_id == user_id)
            .order_by(AgentIntentLog.created_at.desc())
            .limit(limit)
        ).all()
        
        return {
            "customer_id": user_id,
            "interactions": [
                {
                    "id": interaction.id,
                    "intent": interaction.intent,
                    "message": interaction.message,
                    "confidence": interaction.confidence,
                    "created_at": interaction.created_at
                }
                for interaction in interactions
            ]
        }

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from datetime import datetime, timedelta
from sqlmodel import Session, select, func
from app.db.database import engine
from app.models.user import User
from app.models.subscription import Subscription
from app.models.invoice import Invoice
from app.models.problems import Problem
from app.models.packagechangerequest import PackageChangeRequest
from app.models.agentintentlog import AgentIntentLog

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    responses={404: {"description": "Not found"}},
)

@router.get("/stats")
def get_dashboard_stats():
    """Çağrı merkezi dashboard için temel istatistikler"""
    with Session(engine) as session:
        # Kullanıcı istatistikleri
        total_users = session.exec(select(func.count(User.id))).first()
        active_users = session.exec(select(func.count(User.id)).where(User.is_active == True)).first()
        
        # Abonelik istatistikleri
        total_subscriptions = session.exec(select(func.count(Subscription.id))).first()
        active_subscriptions = session.exec(select(func.count(Subscription.id)).where(Subscription.is_active == True)).first()
        
        # Fatura istatistikleri
        unpaid_invoices = session.exec(select(func.count(Invoice.id)).where(Invoice.status == "pending")).first()
        overdue_invoices = session.exec(select(func.count(Invoice.id)).where(Invoice.status == "overdue")).first()
        
        # Problem istatistikleri
        total_problems = session.exec(select(func.count(Problem.id))).first()
        pending_problems = session.exec(select(func.count(Problem.id)).where(Problem.status == "pending")).first()
        
        # Paket değişiklik talepleri
        pending_requests = session.exec(select(func.count(PackageChangeRequest.id)).where(PackageChangeRequest.status == "pending")).first()
        
        return {
            "users": {
                "total": total_users or 0,
                "active": active_users or 0,
                "inactive": (total_users or 0) - (active_users or 0)
            },
            "subscriptions": {
                "total": total_subscriptions or 0,
                "active": active_subscriptions or 0,
                "inactive": (total_subscriptions or 0) - (active_subscriptions or 0)
            },
            "invoices": {
                "unpaid": unpaid_invoices or 0,
                "overdue": overdue_invoices or 0
            },
            "problems": {
                "total": total_problems or 0,
                "pending": pending_problems or 0
            },
            "package_requests": {
                "pending": pending_requests or 0
            }
        }

@router.get("/recent-activities")
def get_recent_activities(limit: int = 20):
    """Son aktiviteleri getir"""
    with Session(engine) as session:
        # Son agent logları
        recent_logs = session.exec(
            select(AgentIntentLog)
            .order_by(AgentIntentLog.created_at.desc())
            .limit(limit)
        ).all()
        
        # Son paket değişiklik talepleri
        recent_requests = session.exec(
            select(PackageChangeRequest)
            .order_by(PackageChangeRequest.requested_at.desc())
            .limit(limit)
        ).all()
        
        return {
            "recent_agent_logs": [
                {
                    "id": log.id,
                    "user_id": log.user_id,
                    "intent": log.intent,
                    "message": log.message[:100] + "..." if len(log.message) > 100 else log.message,
                    "created_at": log.created_at
                }
                for log in recent_logs
            ],
            "recent_package_requests": [
                {
                    "id": req.id,
                    "user_id": req.user_id,
                    "status": req.status,
                    "requested_at": req.requested_at
                }
                for req in recent_requests
            ]
        }

@router.get("/user/{user_id}/summary")
def get_user_summary(user_id: int):
    """Belirli bir kullanıcı için özet bilgiler"""
    with Session(engine) as session:
        # Kullanıcı bilgileri
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Aktif abonelik
        active_subscription = session.exec(
            select(Subscription).where(
                Subscription.user_id == user_id,
                Subscription.is_active == True
            )
        ).first()
        
        # Fatura sayısı
        invoice_count = session.exec(
            select(func.count(Invoice.id)).where(Invoice.user_id == user_id)
        ).first()
        
        # Ödenmemiş fatura sayısı
        unpaid_invoice_count = session.exec(
            select(func.count(Invoice.id)).where(
                Invoice.user_id == user_id,
                Invoice.status == "pending"
            )
        ).first()
        
        # Son agent logları
        recent_logs = session.exec(
            select(AgentIntentLog)
            .where(AgentIntentLog.user_id == user_id)
            .order_by(AgentIntentLog.created_at.desc())
            .limit(5)
        ).all()
        
        return {
            "user": {
                "id": user.id,
                "name": f"{user.name} {user.surname}",
                "phone": user.phone_number,
                "email": user.email,
                "is_active": user.is_active
            },
            "subscription": {
                "has_active": active_subscription is not None,
                "package_id": active_subscription.package_id if active_subscription else None,
                "start_date": active_subscription.start_date if active_subscription else None,
                "end_date": active_subscription.end_date if active_subscription else None,
                "contract_months": active_subscription.contract_months if active_subscription else None
            },
            "invoices": {
                "total": invoice_count or 0,
                "unpaid": unpaid_invoice_count or 0
            },
            "recent_interactions": [
                {
                    "intent": log.intent,
                    "message": log.message[:100] + "..." if len(log.message) > 100 else log.message,
                    "created_at": log.created_at
                }
                for log in recent_logs
            ]
        }

@router.get("/problems/urgent")
def get_urgent_problems():
    """Acil problemleri getir"""
    with Session(engine) as session:
        # Süresi geçmiş problemler
        overdue_problems = session.exec(
            select(Problem).where(
                Problem.estimated_completion_time < datetime.utcnow(),
                Problem.status != "completed"
            )
        ).all()
        
        # Yüksek öncelikli problemler
        high_priority_problems = session.exec(
            select(Problem).where(
                Problem.priority.in_(["high", "critical"]),
                Problem.status != "completed"
            )
        ).all()
        
        return {
            "overdue_problems": [
                {
                    "id": p.id,
                    "location": p.location,
                    "problem": p.problem[:100] + "..." if len(p.problem) > 100 else p.problem,
                    "estimated_completion_time": p.estimated_completion_time,
                    "priority": p.priority,
                    "status": p.status
                }
                for p in overdue_problems
            ],
            "high_priority_problems": [
                {
                    "id": p.id,
                    "location": p.location,
                    "problem": p.problem[:100] + "..." if len(p.problem) > 100 else p.problem,
                    "estimated_completion_time": p.estimated_completion_time,
                    "priority": p.priority,
                    "status": p.status
                }
                for p in high_priority_problems
            ]
        }

@router.get("/revenue/monthly")
def get_monthly_revenue():
    """Aylık gelir istatistikleri"""
    with Session(engine) as session:
        # Son 12 ayın geliri
        monthly_revenue = []
        for i in range(12):
            month_start = datetime.utcnow().replace(day=1) - timedelta(days=30*i)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            revenue = session.exec(
                select(func.sum(Invoice.total_amount)).where(
                    Invoice.status == "paid",
                    Invoice.created_at >= month_start,
                    Invoice.created_at <= month_end
                )
            ).first()
            
            monthly_revenue.append({
                "month": month_start.strftime("%Y-%m"),
                "revenue": float(revenue or 0)
            })
        
        return {"monthly_revenue": list(reversed(monthly_revenue))}

from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime, timezone, timedelta
import re
from app.models.subscription import Subscription
from app.db.database import engine

from app.models.packagechangerequest import PackageChangeRequest
from app.crud.package_crud import get_package_by_id


def parse_commitment_duration(commitment: str) -> int:
    """Taahhüt süresini ay cinsinden parse et"""
    if not commitment or commitment.lower() == "yok":
        return 0
    
    # "12 ay", "24 ay" gibi formatları parse et
    match = re.search(r'(\d+)\s*ay', commitment.lower())
    if match:
        return int(match.group(1))
    
    return 0


def get_subscriptions() -> List[Subscription]:
    """Tüm abonelikleri getir"""
    with Session(engine) as session:
        return session.exec(select(Subscription)).all()


def get_subscription_by_id(subscription_id: int) -> Optional[Subscription]:
    """ID'ye göre abonelik getir"""
    with Session(engine) as session:
        return session.get(Subscription, subscription_id)


def get_subscriptions_by_user(user_id: int) -> List[Subscription]:
    """Kullanıcıya göre abonelikleri getir"""
    with Session(engine) as session:
        query = select(Subscription).where(Subscription.user_id == user_id)
        return session.exec(query).all()


def get_active_subscriptions() -> List[Subscription]:
    """Aktif abonelikleri getir"""
    with Session(engine) as session:
        query = select(Subscription).where(Subscription.is_active == True)
        return session.exec(query).all()


def get_subscriptions_by_package(package_id: int) -> List[Subscription]:
    """Pakete göre abonelikleri getir"""
    with Session(engine) as session:
        query = select(Subscription).where(Subscription.package_id == package_id)
        return session.exec(query).all()


def create_subscription(packagechangereq: PackageChangeRequest) -> Subscription:
    """Yeni abonelik oluştur"""
    try:
        subscription = Subscription()
        subscription.user_id = packagechangereq.user_id
        subscription.package_id = packagechangereq.requested_package_id

        # Paket bilgilerini al
        package = get_package_by_id(packagechangereq.requested_package_id)
        
        subscription.is_active = True
        subscription.start_date = datetime.now(timezone.utc)
        
        # Taahhüt süresini hesapla ve end_date'i ayarla
        if package and package.commitment:
            commitment_months = parse_commitment_duration(package.commitment)
            subscription.contract_months = commitment_months  # Taahhüt süresini kaydet
            
            if commitment_months > 0:
                # Yaklaşık olarak ay hesabı (30 gün * ay sayısı)
                subscription.end_date = subscription.start_date + timedelta(days=commitment_months * 30)
            else:
                # Taahhüt yok ise end_date None olabilir veya çok uzak bir tarih
                subscription.end_date = None
        else:
            subscription.contract_months = None
            subscription.end_date = None
            
        subscription.created_at = datetime.now(timezone.utc)
        subscription.updated_at = datetime.now(timezone.utc)
        
        with Session(engine) as session:
            session.add(subscription)
            session.commit()
            session.refresh(subscription)
            print(f"Subscription created successfully: ID={subscription.id}")
            return subscription
    except Exception as e:
        print(f"Error creating subscription: {e}")
        raise e


def update_subscription(subscription_id: int, subscription_data: dict) -> Optional[Subscription]:
    """Abonelik bilgilerini güncelle"""
    with Session(engine) as session:
        subscription = session.get(Subscription, subscription_id)
        if subscription:
            for key, value in subscription_data.items():
                setattr(subscription, key, value)
            subscription.updated_at = datetime.utcnow()
            session.add(subscription)
            session.commit()
            session.refresh(subscription)
            return subscription
        return None


def delete_subscription(subscription_id: int) -> bool:
    """Abonelik sil"""
    with Session(engine) as session:
        subscription = session.get(Subscription, subscription_id)
        if subscription:
            session.delete(subscription)
            session.commit()
            return True
        return False


def deactivate_subscription(subscription_id: int) -> Optional[Subscription]:
    """Aboneliği deaktive et"""
    with Session(engine) as session:
        subscription = session.get(Subscription, subscription_id)
        if subscription:
            subscription.is_active = False
            subscription.end_date = datetime.utcnow()
            subscription.updated_at = datetime.utcnow()
            session.add(subscription)
            session.commit()
            session.refresh(subscription)
            return subscription
        return None


def get_expiring_subscriptions(days: int = 30) -> List[Subscription]:
    """Belirli gün içinde süresi dolacak abonelikleri getir"""
    target_date = datetime.utcnow() + datetime.timedelta(days=days)
    with Session(engine) as session:
        query = select(Subscription).where(
            Subscription.end_date <= target_date,
            Subscription.is_active == True
        )
        return session.exec(query).all()


def get_user_active_subscription(user_id: int) -> Optional[Subscription]:
    """Kullanıcının aktif aboneliğini getir"""
    with Session(engine) as session:
        query = select(Subscription).options(selectinload(Subscription.package)).where(
            Subscription.user_id == user_id,
            Subscription.is_active == True
        )
        return session.exec(query).first()

def get_commitment_time(user_id: int) -> Optional[datetime]:
    """Kullanıcının taahhütünün ne zaman biteceğinin zamanını getirir"""
    with Session(engine) as session:
        query = select(Subscription.end_date).where(
            Subscription.user_id == user_id,
            Subscription.is_active == True
        )
        return session.exec(query).first()

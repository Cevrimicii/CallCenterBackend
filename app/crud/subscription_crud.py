from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from app.models.subscription import Subscription
from app.db.database import engine


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


def create_subscription(subscription: Subscription) -> Subscription:
    """Yeni abonelik oluştur"""
    with Session(engine) as session:
        session.add(subscription)
        session.commit()
        session.refresh(subscription)
        return subscription


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
        query = select(Subscription).where(
            Subscription.user_id == user_id,
            Subscription.is_active == True
        )
        return session.exec(query).first()

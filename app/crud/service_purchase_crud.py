from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from app.models.servicepurchase import ServicePurchase
from app.db.database import engine


def get_service_purchases() -> List[ServicePurchase]:
    """Tüm hizmet satın alımlarını getir"""
    with Session(engine) as session:
        return session.exec(select(ServicePurchase)).all()


def get_service_purchase_by_id(purchase_id: int) -> Optional[ServicePurchase]:
    """ID'ye göre hizmet satın alımı getir"""
    with Session(engine) as session:
        return session.get(ServicePurchase, purchase_id)


def get_service_purchases_by_user(user_id: int) -> List[ServicePurchase]:
    """Kullanıcıya göre hizmet satın alımlarını getir"""
    with Session(engine) as session:
        query = select(ServicePurchase).where(ServicePurchase.user_id == user_id)
        return session.exec(query).all()


def get_service_purchases_by_type(service_type: str) -> List[ServicePurchase]:
    """Hizmet tipine göre satın alımları getir"""
    with Session(engine) as session:
        query = select(ServicePurchase).where(ServicePurchase.service_type == service_type)
        return session.exec(query).all()


def get_service_purchases_by_user_and_type(user_id: int, service_type: str) -> List[ServicePurchase]:
    """Kullanıcı ve hizmet tipine göre satın alımları getir"""
    with Session(engine) as session:
        query = select(ServicePurchase).where(
            ServicePurchase.user_id == user_id,
            ServicePurchase.service_type == service_type
        )
        return session.exec(query).all()


def create_service_purchase(service_purchase: ServicePurchase) -> ServicePurchase:
    """Yeni hizmet satın alımı oluştur"""
    with Session(engine) as session:
        session.add(service_purchase)
        session.commit()
        session.refresh(service_purchase)
        return service_purchase


def update_service_purchase(purchase_id: int, purchase_data: dict) -> Optional[ServicePurchase]:
    """Hizmet satın alımı bilgilerini güncelle"""
    with Session(engine) as session:
        service_purchase = session.get(ServicePurchase, purchase_id)
        if service_purchase:
            for key, value in purchase_data.items():
                setattr(service_purchase, key, value)
            session.add(service_purchase)
            session.commit()
            session.refresh(service_purchase)
            return service_purchase
        return None


def delete_service_purchase(purchase_id: int) -> bool:
    """Hizmet satın alımı sil"""
    with Session(engine) as session:
        service_purchase = session.get(ServicePurchase, purchase_id)
        if service_purchase:
            session.delete(service_purchase)
            session.commit()
            return True
        return False


def get_service_purchases_by_date_range(start_date: datetime, end_date: datetime) -> List[ServicePurchase]:
    """Belirli bir tarih aralığındaki hizmet satın alımlarını getir"""
    with Session(engine) as session:
        query = select(ServicePurchase).where(
            ServicePurchase.purchase_date >= start_date,
            ServicePurchase.purchase_date <= end_date
        )
        return session.exec(query).all()


def get_total_spent_by_user(user_id: int) -> float:
    """Kullanıcının toplam harcamasını hesapla"""
    with Session(engine) as session:
        query = select(ServicePurchase).where(ServicePurchase.user_id == user_id)
        purchases = session.exec(query).all()
        return sum(purchase.purchase_price for purchase in purchases)

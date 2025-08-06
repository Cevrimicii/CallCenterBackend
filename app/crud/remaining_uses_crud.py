from sqlmodel import Session, select
from typing import List, Optional
from app.models.remaininguses import RemainingUses
from app.db.database import engine


def get_remaining_uses() -> List[RemainingUses]:
    """Tüm kalan kullanımları getir"""
    with Session(engine) as session:
        return session.exec(select(RemainingUses)).all()


def get_remaining_uses_by_id(remaining_uses_id: int) -> Optional[RemainingUses]:
    """ID'ye göre kalan kullanım getir"""
    with Session(engine) as session:
        return session.get(RemainingUses, remaining_uses_id)


def get_remaining_uses_by_user(user_id: int) -> List[RemainingUses]:
    """Kullanıcıya göre kalan kullanımları getir"""
    with Session(engine) as session:
        query = select(RemainingUses).where(RemainingUses.user_id == user_id)
        return session.exec(query).all()


def get_remaining_uses_by_service(user_id: int, service_type: str) -> Optional[RemainingUses]:
    """Kullanıcı ve hizmet tipine göre kalan kullanım getir"""
    with Session(engine) as session:
        query = select(RemainingUses).where(
            RemainingUses.user_id == user_id,
            RemainingUses.service_type == service_type
        )
        return session.exec(query).first()


def create_remaining_uses(remaining_uses: RemainingUses) -> RemainingUses:
    """Yeni kalan kullanım oluştur"""
    with Session(engine) as session:
        session.add(remaining_uses)
        session.commit()
        session.refresh(remaining_uses)
        return remaining_uses


def update_remaining_uses(remaining_uses_id: int, remaining_uses_data: dict) -> Optional[RemainingUses]:
    """Kalan kullanım bilgilerini güncelle"""
    with Session(engine) as session:
        remaining_uses = session.get(RemainingUses, remaining_uses_id)
        if remaining_uses:
            for key, value in remaining_uses_data.items():
                setattr(remaining_uses, key, value)
            session.add(remaining_uses)
            session.commit()
            session.refresh(remaining_uses)
            return remaining_uses
        return None


def delete_remaining_uses(remaining_uses_id: int) -> bool:
    """Kalan kullanım sil"""
    with Session(engine) as session:
        remaining_uses = session.get(RemainingUses, remaining_uses_id)
        if remaining_uses:
            session.delete(remaining_uses)
            session.commit()
            return True
        return False


def decrease_remaining_count(user_id: int, service_type: str, count: int = 1) -> Optional[RemainingUses]:
    """Kalan kullanım sayısını azalt"""
    with Session(engine) as session:
        query = select(RemainingUses).where(
            RemainingUses.user_id == user_id,
            RemainingUses.service_type == service_type
        )
        remaining_uses = session.exec(query).first()
        if remaining_uses and remaining_uses.remaining_count >= count:
            remaining_uses.remaining_count -= count
            session.add(remaining_uses)
            session.commit()
            session.refresh(remaining_uses)
            return remaining_uses
        return None


def increase_remaining_count(user_id: int, service_type: str, count: int) -> Optional[RemainingUses]:
    """Kalan kullanım sayısını artır"""
    with Session(engine) as session:
        query = select(RemainingUses).where(
            RemainingUses.user_id == user_id,
            RemainingUses.service_type == service_type
        )
        remaining_uses = session.exec(query).first()
        if remaining_uses:
            remaining_uses.remaining_count += count
            remaining_uses.total_allocated += count
            session.add(remaining_uses)
            session.commit()
            session.refresh(remaining_uses)
            return remaining_uses
        return None

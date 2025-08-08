from sqlmodel import Session, select
from typing import List, Optional
from app.models.user import User
from app.db.database import engine


def get_users() -> List[User]:
    """Tüm kullanıcıları getir"""
    with Session(engine) as session:
        return session.exec(select(User)).all()


def get_user_by_id(user_id: int) -> Optional[User]:
    """ID'ye göre kullanıcı getir"""
    with Session(engine) as session:
        return session.get(User, user_id)


def get_user_by_phone(phone_number: str) -> Optional[User]:
    """Telefon numarasına göre kullanıcı getir"""
    with Session(engine) as session:
        query = select(User).where(User.phone_number == phone_number)
        return session.exec(query).first()

def create_user(user: User) -> User:
    """Yeni kullanıcı oluştur"""
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def update_user(user_id: int, user_data: dict) -> Optional[User]:
    """Kullanıcı bilgilerini güncelle"""
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        return None


def delete_user(user_id: int) -> bool:
    """Kullanıcı sil"""
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user:
            session.delete(user)
            session.commit()
            return True
        return False


def get_users_by_package(package_id: int) -> List[User]:
    """Belirli bir pakete sahip kullanıcıları getir"""
    with Session(engine) as session:
        query = select(User).where(User.package_id == package_id)
        return session.exec(query).all()

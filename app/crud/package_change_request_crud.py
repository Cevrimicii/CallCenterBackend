from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from app.models.packagechangerequest import PackageChangeRequest
from app.db.database import engine


def get_package_change_requests() -> List[PackageChangeRequest]:
    """Tüm paket değişiklik taleplerini getir"""
    with Session(engine) as session:
        return session.exec(select(PackageChangeRequest)).all()


def get_package_change_request_by_id(request_id: int) -> Optional[PackageChangeRequest]:
    """ID'ye göre paket değişiklik talebi getir"""
    with Session(engine) as session:
        return session.get(PackageChangeRequest, request_id)


def get_package_change_requests_by_user(user_id: int) -> List[PackageChangeRequest]:
    """Kullanıcıya göre paket değişiklik taleplerini getir"""
    with Session(engine) as session:
        query = select(PackageChangeRequest).where(PackageChangeRequest.user_id == user_id)
        return session.exec(query).all()


def get_package_change_requests_by_status(status: str) -> List[PackageChangeRequest]:
    """Duruma göre paket değişiklik taleplerini getir"""
    with Session(engine) as session:
        query = select(PackageChangeRequest).where(PackageChangeRequest.status == status)
        return session.exec(query).all()


def get_pending_package_change_requests() -> List[PackageChangeRequest]:
    """Bekleyen paket değişiklik taleplerini getir"""
    with Session(engine) as session:
        query = select(PackageChangeRequest).where(PackageChangeRequest.status == "pending")
        return session.exec(query).all()


def create_package_change_request(package_change_request: PackageChangeRequest) -> PackageChangeRequest:
    """Yeni paket değişiklik talebi oluştur"""
    with Session(engine) as session:
        session.add(package_change_request)
        session.commit()
        session.refresh(package_change_request)
        return package_change_request


def update_package_change_request(request_id: int, request_data: dict) -> Optional[PackageChangeRequest]:
    """Paket değişiklik talebi bilgilerini güncelle"""
    with Session(engine) as session:
        package_change_request = session.get(PackageChangeRequest, request_id)
        if package_change_request:
            for key, value in request_data.items():
                setattr(package_change_request, key, value)
            session.add(package_change_request)
            session.commit()
            session.refresh(package_change_request)
            return package_change_request
        return None


def delete_package_change_request(request_id: int) -> bool:
    """Paket değişiklik talebi sil"""
    with Session(engine) as session:
        package_change_request = session.get(PackageChangeRequest, request_id)
        if package_change_request:
            session.delete(package_change_request)
            session.commit()
            return True
        return False


def approve_package_change_request(request_id: int) -> Optional[PackageChangeRequest]:
    """Paket değişiklik talebini onayla"""
    with Session(engine) as session:
        package_change_request = session.get(PackageChangeRequest, request_id)
        if package_change_request:
            package_change_request.status = "approved"
            session.add(package_change_request)
            session.commit()
            session.refresh(package_change_request)
            return package_change_request
        return None


def reject_package_change_request(request_id: int) -> Optional[PackageChangeRequest]:
    """Paket değişiklik talebini reddet"""
    with Session(engine) as session:
        package_change_request = session.get(PackageChangeRequest, request_id)
        if package_change_request:
            package_change_request.status = "rejected"
            session.add(package_change_request)
            session.commit()
            session.refresh(package_change_request)
            return package_change_request
        return None

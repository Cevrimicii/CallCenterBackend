from sqlmodel import Session, select
from typing import List, Optional
from app.models.package import Package
from app.db.database import engine


def get_packages() -> List[Package]:
    """Tüm paketleri getir"""
    with Session(engine) as session:
        return session.exec(select(Package)).all()


def get_package_by_id(package_id: int) -> Optional[Package]:
    """ID'ye göre paket getir"""
    with Session(engine) as session:
        return session.get(Package, package_id)


def get_packages_by_type(package_type: str) -> List[Package]:
    """Tipe göre paketleri getir"""
    with Session(engine) as session:
        query = select(Package).where(Package.type == package_type)
        return session.exec(query).all()


def create_package(package: Package) -> Package:
    """Yeni paket oluştur"""
    with Session(engine) as session:
        session.add(package)
        session.commit()
        session.refresh(package)
        return package


def update_package(package_id: int, package_data: dict) -> Optional[Package]:
    """Paket bilgilerini güncelle"""
    with Session(engine) as session:
        package = session.get(Package, package_id)
        if package:
            for key, value in package_data.items():
                setattr(package, key, value)
            session.add(package)
            session.commit()
            session.refresh(package)
            return package
        return None


def delete_package(package_id: int) -> bool:
    """Paket sil"""
    with Session(engine) as session:
        package = session.get(Package, package_id)
        if package:
            session.delete(package)
            session.commit()
            return True
        return False


def get_package_by_user_phone(phone_number: str) -> Optional[Package]:
    """Kullanıcının telefon numarasına göre paket getir"""
    with Session(engine) as session:
        from app.models.user import User
        query = select(User).where(User.phone_number == phone_number)
        user = session.exec(query).first()
        if user and user.package_id:
            return session.get(Package, user.package_id)
        return None

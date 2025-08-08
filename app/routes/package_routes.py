from fastapi import APIRouter, HTTPException
from typing import List
from sqlmodel import Session, select
from app.db.database import engine
from app.crud.package_crud import (
    get_packages,
    get_package_by_id,
    create_package,
    update_package,
    delete_package,
)
from app.models.package import Package

router = APIRouter(
    prefix="/packages",
    tags=["packages"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Package])
def get_all_packages():
    """Tüm paketleri getir"""
    return get_packages()

@router.get("/active", response_model=List[Package])
def get_active_packages_list():
    """Aktif paketleri getir"""
    with Session(engine) as session:
        query = select(Package).where(Package.is_active == True)
        return session.exec(query).all()

@router.get("/{name}", response_model=List[Package])
def get_package_by_name(package_name: str):
    """Verilen isime göre paketleri getirir"""
    with Session(engine) as session:
        query = select(Package).where(Package.is_active == True).where(Package.name == package_name)
        return session.exec(query).all()

@router.get("/{package_type}", response_model=List[Package])
def get_package_by_type(package_type: str):
    """Verilen tipe göre paketleri getirir"""
    with Session(engine) as session:
        query = select(Package).where(Package.is_active == True).where(Package.type == package_type)
        return session.exec(query).all()

@router.get("/{package_id}", response_model=Package)
def get_package(package_id: int):
    """ID'ye göre paket getir"""
    package = get_package_by_id(package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    return package

@router.post("/", response_model=Package)
def add_package(package: Package):
    """Yeni paket oluştur"""
    return create_package(package)

@router.put("/{package_id}", response_model=Package)
def update_package_info(package_id: int, package_data: dict):
    """Paket bilgilerini güncelle"""
    package = update_package(package_id, package_data)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    return package

@router.delete("/{package_id}")
def delete_package_by_id(package_id: int):
    """Paket sil"""
    success = delete_package(package_id)
    if not success:
        raise HTTPException(status_code=404, detail="Package not found")
    return {"message": "Package deleted successfully"}
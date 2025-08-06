from fastapi import APIRouter, HTTPException
from typing import List
from app.crud.user_crud import (
    get_users as get_all_users,
    get_user_by_id,
    get_user_by_phone,
    create_user,
    update_user,
    delete_user,
    get_user_current_package
)
from app.models.user import User
from app.models.package import Package

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[User])
def get_users():
    """Tüm kullanıcıları getir"""
    return get_all_users()

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    """ID'ye göre kullanıcı getir"""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/phone/{phone_number}", response_model=User)
def get_user_by_phone_number(phone_number: str):
    """Telefon numarasına göre kullanıcı getir"""
    user = get_user_by_phone(phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{user_id}/package", response_model=Package)
def get_user_package(user_id: int):
    """Kullanıcının mevcut paketini getir"""
    package = get_user_current_package(user_id)
    if not package:
        raise HTTPException(status_code=404, detail="No active package found")
    return package

@router.post("/", response_model=User)
def add_user(user: User):
    """Yeni kullanıcı oluştur"""
    return create_user(user)

@router.put("/{user_id}", response_model=User)
def update_user_info(user_id: int, user_data: dict):
    """Kullanıcı bilgilerini güncelle"""
    user = update_user(user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
def delete_user_by_id(user_id: int):
    """Kullanıcı sil"""
    success = delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
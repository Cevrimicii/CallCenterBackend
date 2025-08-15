from fastapi import APIRouter, HTTPException, Request
from typing import List
from app.crud.user_crud import (
    get_users as get_all_users,
    get_user_by_id,
    get_user_by_phone,
    create_user,
    update_user,
    delete_user,
)
from app.crud.subscription_crud import get_user_active_subscription
from app.models.user import User
from app.models.package import Package
from app.utils.logging_config import get_logger, log_business_operation, log_error

logger = get_logger('app.routes.user')

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[User])
def get_users(request: Request):
    """Tüm kullanıcıları getir"""
    try:
        client_ip = request.client.host if request.client else "unknown"
        logger.info(f"Fetching all users - IP: {client_ip}")
        result = get_all_users()
        log_business_operation("GET_ALL_USERS", f"Retrieved {len(result)} users")
        return result
    except Exception as e:
        log_error(e, "Error fetching all users")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, request: Request):
    """ID'ye göre kullanıcı getir"""
    try:
        client_ip = request.client.host if request.client else "unknown"
        logger.info(f"Fetching user by ID: {user_id} - IP: {client_ip}")
        user = get_user_by_id(user_id)
        if not user:
            logger.warning(f"User not found with ID: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        log_business_operation("GET_USER_BY_ID", f"User {user_id} retrieved", user_id=user_id)
        return user
    except HTTPException:
        raise
    except Exception as e:
        log_error(e, f"Error fetching user by ID: {user_id}")
        raise HTTPException(status_code=500, detail="Internal server error")

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
    subscription = get_user_active_subscription(user_id)
    if subscription and subscription.package:
        return subscription.package
    else:
        raise HTTPException(status_code=404, detail="No active package found")

@router.get("/phone/{phone_number}/package", response_model=Package)
def get_user_package_by_phone(phone_number: str):
    """Telefon numarasına göre kullanıcının mevcut paketini getir"""
    # Önce telefon numarasından kullanıcıyı bul
    user = get_user_by_phone(phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Kullanıcının aktif aboneliğini getir
    subscription = get_user_active_subscription(user.id)
    if subscription and subscription.package:
        return subscription.package
    else:
        raise HTTPException(status_code=404, detail="No active package found for this user")

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
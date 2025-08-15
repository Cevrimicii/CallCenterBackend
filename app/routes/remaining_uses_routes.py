from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from app.crud.remaining_uses_crud import (
    get_remaining_uses,
    get_remaining_uses_by_id,
    get_remaining_uses_by_user,
    get_remaining_uses_by_service,
    create_remaining_uses,
    update_remaining_uses,
    delete_remaining_uses,
    decrease_remaining_count,
    increase_remaining_count
)
from app.crud.user_crud import get_user_by_phone
from app.models.remaininguses import RemainingUses

router = APIRouter(
    prefix="/remaining-uses",
    tags=["remaining-uses"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[RemainingUses])
def get_all_remaining_uses():
    """Tüm kalan kullanımları getir"""
    return get_remaining_uses()

@router.get("/{remaining_uses_id}", response_model=RemainingUses)
def get_remaining_use(remaining_uses_id: int):
    """ID'ye göre kalan kullanım getir"""
    remaining_use = get_remaining_uses_by_id(remaining_uses_id)
    if not remaining_use:
        raise HTTPException(status_code=404, detail="Remaining uses not found")
    return remaining_use

@router.get("/user/{user_id}", response_model=List[RemainingUses])
def get_user_remaining_uses(user_id: int):
    """Kullanıcının kalan kullanımlarını getir"""
    return get_remaining_uses_by_user(user_id)

@router.get("/phone/{phone_number}", response_model=List[RemainingUses])
def get_user_remaining_uses_by_phone(phone_number: str):
    """Telefon numarasına göre kullanıcının kalan kullanımlarını getir"""
    # Önce telefon numarasından kullanıcıyı bul
    user = get_user_by_phone(phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Kullanıcının kalan kullanımlarını getir
    return get_remaining_uses_by_user(user.id)

@router.get("/user/{user_id}/service/{service_type}", response_model=RemainingUses)
def get_user_service_remaining_uses(user_id: int, service_type: str):
    """Kullanıcının belirli hizmet için kalan kullanımını getir"""
    remaining_use = get_remaining_uses_by_service(user_id, service_type)
    if not remaining_use:
        raise HTTPException(status_code=404, detail="No remaining uses found for this service")
    return remaining_use

@router.get("/phone/{phone_number}/service/{service_type}", response_model=RemainingUses)
def get_user_service_remaining_uses_by_phone(phone_number: str, service_type: str):
    """Telefon numarasına göre kullanıcının belirli hizmet için kalan kullanımını getir"""
    # Önce telefon numarasından kullanıcıyı bul
    user = get_user_by_phone(phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Kullanıcının belirli hizmet için kalan kullanımını getir
    remaining_use = get_remaining_uses_by_service(user.id, service_type)
    if not remaining_use:
        raise HTTPException(status_code=404, detail="No remaining uses found for this service")
    return remaining_use

@router.post("/", response_model=RemainingUses)
def create_new_remaining_uses(remaining_uses: RemainingUses):
    """Yeni kalan kullanım oluştur"""
    return create_remaining_uses(remaining_uses)

@router.put("/{remaining_uses_id}", response_model=RemainingUses)
def update_remaining_uses_info(remaining_uses_id: int, remaining_uses_data: dict):
    """Kalan kullanım bilgilerini güncelle"""
    remaining_uses = update_remaining_uses(remaining_uses_id, remaining_uses_data)
    if not remaining_uses:
        raise HTTPException(status_code=404, detail="Remaining uses not found")
    return remaining_uses

@router.delete("/{remaining_uses_id}")
def delete_remaining_uses_by_id(remaining_uses_id: int):
    """Kalan kullanım sil"""
    success = delete_remaining_uses(remaining_uses_id)
    if not success:
        raise HTTPException(status_code=404, detail="Remaining uses not found")
    return {"message": "Remaining uses deleted successfully"}

@router.put("/user/{user_id}/service/{service_type}/decrease")
def decrease_user_remaining_count(user_id: int, service_type: str, count: int = 1):
    """Kullanıcının kalan kullanım sayısını azalt"""
    remaining_uses = decrease_remaining_count(user_id, service_type, count)
    if not remaining_uses:
        raise HTTPException(status_code=404, detail="Insufficient remaining uses or service not found")
    return {"message": f"Decreased {count} from remaining uses", "remaining_count": remaining_uses.remaining_count}

@router.put("/phone/{phone_number}/service/{service_type}/decrease")
def decrease_user_remaining_count_by_phone(phone_number: str, service_type: str, count: int = 1):
    """Telefon numarasına göre kullanıcının kalan kullanım sayısını azalt"""
    # Önce telefon numarasından kullanıcıyı bul
    user = get_user_by_phone(phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    remaining_uses = decrease_remaining_count(user.id, service_type, count)
    if not remaining_uses:
        raise HTTPException(status_code=404, detail="Insufficient remaining uses or service not found")
    return {"message": f"Decreased {count} from remaining uses", "remaining_count": remaining_uses.remaining_count}

@router.put("/user/{user_id}/service/{service_type}/increase")
def increase_user_remaining_count(user_id: int, service_type: str, count: int):
    """Kullanıcının kalan kullanım sayısını artır"""
    remaining_uses = increase_remaining_count(user_id, service_type, count)
    if not remaining_uses:
        raise HTTPException(status_code=404, detail="Service not found for user")
    return {"message": f"Added {count} to remaining uses", "remaining_count": remaining_uses.remaining_count}

@router.put("/phone/{phone_number}/service/{service_type}/increase")
def increase_user_remaining_count_by_phone(phone_number: str, service_type: str, count: int):
    """Telefon numarasına göre kullanıcının kalan kullanım sayısını artır"""
    # Önce telefon numarasından kullanıcıyı bul
    user = get_user_by_phone(phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    remaining_uses = increase_remaining_count(user.id, service_type, count)
    if not remaining_uses:
        raise HTTPException(status_code=404, detail="Service not found for user")
    return {"message": f"Added {count} to remaining uses", "remaining_count": remaining_uses.remaining_count}

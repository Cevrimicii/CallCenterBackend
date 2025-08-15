from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from app.crud.service_purchase_crud import (
    get_service_purchases,
    get_service_purchase_by_id,
    get_service_purchases_by_user,
    get_service_purchases_by_type,
    get_service_purchases_by_user_and_type,
    create_service_purchase,
    update_service_purchase,
    delete_service_purchase,
    get_service_purchases_by_date_range,
    get_total_spent_by_user
)
from app.crud.user_crud import get_user_by_phone
from app.models.servicepurchase import ServicePurchase

router = APIRouter(
    prefix="/service-purchases",
    tags=["service-purchases"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[ServicePurchase])
def get_all_service_purchases():
    """Tüm hizmet satın alımlarını getir"""
    return get_service_purchases()

@router.get("/{purchase_id}", response_model=ServicePurchase)
def get_service_purchase(purchase_id: int):
    """ID'ye göre hizmet satın alımı getir"""
    purchase = get_service_purchase_by_id(purchase_id)
    if not purchase:
        raise HTTPException(status_code=404, detail="Service purchase not found")
    return purchase

@router.get("/user/{user_id}", response_model=List[ServicePurchase])
def get_user_service_purchases(user_id: int):
    """Kullanıcının hizmet satın alımlarını getir"""
    return get_service_purchases_by_user(user_id)

@router.get("/phone/{phone_number}", response_model=List[ServicePurchase])
def get_user_service_purchases_by_phone(phone_number: str):
    """Telefon numarasına göre kullanıcının hizmet satın alımlarını getir"""
    # Önce telefon numarasından kullanıcıyı bul
    user = get_user_by_phone(phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Kullanıcının hizmet satın alımlarını getir
    return get_service_purchases_by_user(user.id)

@router.get("/type/{service_type}", response_model=List[ServicePurchase])
def get_purchases_by_service_type(service_type: str):
    """Hizmet tipine göre satın alımları getir"""
    return get_service_purchases_by_type(service_type)

@router.get("/user/{user_id}/type/{service_type}", response_model=List[ServicePurchase])
def get_user_purchases_by_service_type(user_id: int, service_type: str):
    """Kullanıcı ve hizmet tipine göre satın alımları getir"""
    return get_service_purchases_by_user_and_type(user_id, service_type)

@router.get("/phone/{phone_number}/type/{service_type}", response_model=List[ServicePurchase])
def get_user_purchases_by_service_type_by_phone(phone_number: str, service_type: str):
    """Telefon numarasına göre kullanıcı ve hizmet tipine göre satın alımları getir"""
    # Önce telefon numarasından kullanıcıyı bul
    user = get_user_by_phone(phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Kullanıcının belirli hizmet tipi için satın alımlarını getir
    return get_service_purchases_by_user_and_type(user.id, service_type)

@router.post("/", response_model=ServicePurchase)
def create_new_service_purchase(service_purchase: ServicePurchase):
    """Yeni hizmet satın alımı oluştur"""
    return create_service_purchase(service_purchase)

@router.put("/{purchase_id}", response_model=ServicePurchase)
def update_service_purchase_info(purchase_id: int, purchase_data: dict):
    """Hizmet satın alımı bilgilerini güncelle"""
    purchase = update_service_purchase(purchase_id, purchase_data)
    if not purchase:
        raise HTTPException(status_code=404, detail="Service purchase not found")
    return purchase

@router.delete("/{purchase_id}")
def delete_service_purchase_by_id(purchase_id: int):
    """Hizmet satın alımı sil"""
    success = delete_service_purchase(purchase_id)
    if not success:
        raise HTTPException(status_code=404, detail="Service purchase not found")
    return {"message": "Service purchase deleted successfully"}

@router.get("/date-range/{start_date}/{end_date}", response_model=List[ServicePurchase])
def get_purchases_by_date_range(start_date: datetime, end_date: datetime):
    """Belirli bir tarih aralığındaki hizmet satın alımlarını getir"""
    return get_service_purchases_by_date_range(start_date, end_date)

@router.get("/month/{year}/{month}", response_model=List[ServicePurchase])
def get_purchases_by_month(year: int, month: int):
    """Belirli bir aydaki hizmet satın alımlarını getir (örnek: 2024/12 - Aralık 2024)"""
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Month must be between 1 and 12")
    
    # Ayın ilk günü
    start_date = datetime(year, month, 1)
    
    # Ayın son günü - bir sonraki ayın ilk gününden bir gün öncesi
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    
    return get_service_purchases_by_date_range(start_date, end_date)

@router.get("/phone/{phone_number}/month/{year}/{month}", response_model=List[ServicePurchase])
def get_user_purchases_by_month_by_phone(phone_number: str, year: int, month: int):
    """Telefon numarasına göre kullanıcının belirli bir aydaki hizmet satın alımlarını getir"""
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Month must be between 1 and 12")
    
    # Önce telefon numarasından kullanıcıyı bul
    user = get_user_by_phone(phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Ayın ilk günü
    start_date = datetime(year, month, 1)
    
    # Ayın son günü
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    
    # Kullanıcının o aydaki tüm satın alımlarını getir
    all_purchases = get_service_purchases_by_date_range(start_date, end_date)
    
    # Sadece bu kullanıcının satın alımlarını filtrele
    user_purchases = [purchase for purchase in all_purchases if purchase.user_id == user.id]
    
    return user_purchases

@router.get("/user/{user_id}/total-spent")
def get_user_total_spent(user_id: int):
    """Kullanıcının toplam harcamasını getir"""
    total_spent = get_total_spent_by_user(user_id)
    return {"user_id": user_id, "total_spent": total_spent}

@router.get("/phone/{phone_number}/total-spent")
def get_user_total_spent_by_phone(phone_number: str):
    """Telefon numarasına göre kullanıcının toplam harcamasını getir"""
    # Önce telefon numarasından kullanıcıyı bul
    user = get_user_by_phone(phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Kullanıcının toplam harcamasını getir
    total_spent = get_total_spent_by_user(user.id)
    return {"user_id": user.id, "phone_number": phone_number, "total_spent": total_spent}

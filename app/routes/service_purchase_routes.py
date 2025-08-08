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

@router.get("/type/{service_type}", response_model=List[ServicePurchase])
def get_purchases_by_service_type(service_type: str):
    """Hizmet tipine göre satın alımları getir"""
    return get_service_purchases_by_type(service_type)

@router.get("/user/{user_id}/type/{service_type}", response_model=List[ServicePurchase])
def get_user_purchases_by_service_type(user_id: int, service_type: str):
    """Kullanıcı ve hizmet tipine göre satın alımları getir"""
    return get_service_purchases_by_user_and_type(user_id, service_type)

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

@router.get("/user/{user_id}/total-spent")
def get_user_total_spent(user_id: int):
    """Kullanıcının toplam harcamasını getir"""
    total_spent = get_total_spent_by_user(user_id)
    return {"user_id": user_id, "total_spent": total_spent}

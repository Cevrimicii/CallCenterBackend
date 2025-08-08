from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from app.crud.package_change_request_crud import (
    get_package_change_requests,
    get_package_change_request_by_id,
    get_package_change_requests_by_user,
    get_package_change_requests_by_status,
    get_pending_package_change_requests,
    create_package_change_request,
    update_package_change_request,
    delete_package_change_request,
    approve_package_change_request,
    reject_package_change_request
)
from app.models.packagechangerequest import PackageChangeRequest

router = APIRouter(
    prefix="/package-change-requests",
    tags=["package-change-requests"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[PackageChangeRequest])
def get_all_package_change_requests():
    """Tüm paket değişiklik taleplerini getir"""
    return get_package_change_requests()

@router.get("/{request_id}", response_model=PackageChangeRequest)
def get_package_change_request(request_id: int):
    """ID'ye göre paket değişiklik talebi getir"""
    request = get_package_change_request_by_id(request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Package change request not found")
    return request

@router.get("/user/{user_id}", response_model=List[PackageChangeRequest])
def get_user_package_change_requests(user_id: int):
    """Kullanıcının paket değişiklik taleplerini getir"""
    return get_package_change_requests_by_user(user_id)

@router.get("/status/{status}", response_model=List[PackageChangeRequest])
def get_requests_by_status(status: str):
    """Duruma göre paket değişiklik taleplerini getir"""
    return get_package_change_requests_by_status(status)

@router.get("/pending/all", response_model=List[PackageChangeRequest])
def get_pending_requests():
    """Bekleyen paket değişiklik taleplerini getir"""
    return get_pending_package_change_requests()

@router.post("/", response_model=PackageChangeRequest)
def create_new_package_change_request(package_change_request: PackageChangeRequest):
    """Yeni paket değişiklik talebi oluştur"""
    return create_package_change_request(package_change_request)

@router.put("/{request_id}", response_model=PackageChangeRequest)
def update_package_change_request_info(request_id: int, request_data: dict):
    """Paket değişiklik talebi bilgilerini güncelle"""
    request = update_package_change_request(request_id, request_data)
    if not request:
        raise HTTPException(status_code=404, detail="Package change request not found")
    return request

@router.delete("/{request_id}")
def delete_package_change_request_by_id(request_id: int):
    """Paket değişiklik talebi sil"""
    success = delete_package_change_request(request_id)
    if not success:
        raise HTTPException(status_code=404, detail="Package change request not found")
    return {"message": "Package change request deleted successfully"}

@router.put("/{request_id}/approve")
def approve_request(request_id: int):
    """Paket değişiklik talebini onayla"""
    request = approve_package_change_request(request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Package change request not found")
    return {"message": "Package change request approved", "request_id": request.id}

@router.put("/{request_id}/reject")
def reject_request(request_id: int):
    """Paket değişiklik talebini reddet"""
    request = reject_package_change_request(request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Package change request not found")
    return {"message": "Package change request rejected", "request_id": request.id}

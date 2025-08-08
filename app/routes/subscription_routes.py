from fastapi import APIRouter, HTTPException
from typing import List
from app.crud.subscription_crud import (
    get_commitment_time,
    create_subscription,
    deactivate_subscription,
    get_user_active_subscription
)
from app.crud.package_change_request_crud import (
    create_package_change_request,
    approve_package_change_request,
    reject_package_change_request,
    get_package_change_request_by_id
)
from app.models.subscription import Subscription
from app.models.packagechangerequest import PackageChangeRequest

router = APIRouter(
    prefix="/subs",
    tags=["subs"],
    responses={404: {"description": "Not found"}},
)

@router.post("/createsubs")
def create_sub(req: PackageChangeRequest):
    """Öncelikle paket değişikliği isteği gidecek şirket onayladığında sub başlayacak"""
    return create_package_change_request(req)

@router.post("/approve")
def approve_package_change_req(package_change_request_id: int):
    """Kullanıcı paket talebi onaylanır"""
    try:
        # Önce paket değişiklik talebini onayla
        approve_package_change_request(package_change_request_id)
        
        # Paket değişiklik talebini getir
        package_change_request = get_package_change_request_by_id(package_change_request_id)
        
        if package_change_request:
            print(f"Package change request found: {package_change_request}")
            # PackageChangeRequest objesini create_subscription'a geçir
            subscription = create_subscription(package_change_request)
            print(f"Subscription created: {subscription.id}")
            return {"message": "Package change approved and subscription created", "subscription_id": subscription.id}
        else:
            raise HTTPException(status_code=404, detail="Package change request not found")
    except Exception as e:
        print(f"Error in approve_package_change_req: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@router.post("/reject")
def reject_package_change_req(package_change_request_id: int):
    """Kullanıcı paket talebi reddedilir"""
    reject_package_change_request(package_change_request_id)

@router.post("/deactive")
def deactive_package_change_req(sub_id: int):
    """Kullanıcının paket aboneliği deaktive edilir"""
    deactivate_subscription(sub_id)


@router.get("/{user_id}/commitment-time")
def get_users_commitment_time(user_id: int):
    """Kullanıcının paket taahhütünün ne zaman biteceğini getirir"""
    commitment_time = get_commitment_time(user_id)
    if commitment_time:
        return {"user_id": user_id, "commitment_end_date": commitment_time}
    else:
        raise HTTPException(status_code=404, detail="No active subscription found for user")

@router.get("/{user_id}/activesub")
def get_user_active_sub(user_id: int):
    """Kullanıcının aktif aboneliğini döner"""
    subscription = get_user_active_subscription(user_id)
    if subscription:
        return subscription
    else:
        raise HTTPException(status_code=404, detail="No active subscription found for user")
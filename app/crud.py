# Bu dosya artık deprecated. Yeni CRUD operasyonları için aşağıdaki dosyaları kullanın:
# - app.crud.user_crud
# - app.crud.package_crud  
# - app.crud.invoice_crud
# - app.crud.invoice_item_crud
# - app.crud.service_purchase_crud
# - app.crud.remaining_uses_crud
# - app.crud.package_change_request_crud
# - app.crud.agent_intent_log_crud
# - app.crud.problem_crud

# Geçici uyumluluk için mevcut fonksiyonları import ediyoruz
from app.crud.user_crud import get_users as getUsers, create_user, get_user_by_phone
from app.crud.package_crud import get_packages, create_package, get_package_by_user_phone

def get_package_by_user(phoneNumber: str):
    """Eski API uyumluluğu için"""
    return get_package_by_user_phone(phoneNumber)
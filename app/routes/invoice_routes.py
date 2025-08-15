from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from app.crud.invoice_crud import (
    get_active_invoice_by_phone,
    get_invoices,
    get_invoice_by_id,
    get_invoices_by_user,
    get_invoices_by_status,
    get_unpaid_invoices,
    create_invoice,
    update_invoice,
    delete_invoice,
    mark_invoice_as_paid,
    get_invoices_by_period
)
from app.crud.invoice_item_crud import get_invoice_items_by_invoice
from app.crud.user_crud import get_user_by_phone
from app.models.invoice import Invoice
from app.models.invoiceitem import InvoiceItem

router = APIRouter(
    prefix="/invoices",
    tags=["invoices"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Invoice])
def get_all_invoices():
    """Tüm faturaları getir"""
    return get_invoices()

@router.get("/{invoice_id}", response_model=Invoice)
def get_invoice(invoice_id: int):
    """ID'ye göre fatura getir"""
    invoice = get_invoice_by_id(invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.get("/{invoice_id}/items", response_model=List[InvoiceItem])
def get_invoice_items(invoice_id: int):
    """Faturanın kalemlerini getir (fiyatı oluşturan ürünler)"""
    # Önce faturanın var olup olmadığını kontrol et
    invoice = get_invoice_by_id(invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    # Fatura kalemlerini getir
    items = get_invoice_items_by_invoice(invoice_id)
    return items

@router.get("/phone/{phone_number}/items", response_model=List[InvoiceItem])
def get_user_invoice_items_by_phone(phone_number: str):
    """Telefon numarasına göre kullanıcının tüm fatura kalemlerini getir"""
    # Önce telefon numarasından kullanıcıyı bul
    user = get_user_by_phone(phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Kullanıcının tüm faturalarını getir
    user_invoices = get_invoices_by_user(user.id)
    if not user_invoices:
        raise HTTPException(status_code=404, detail="No invoices found for this user")
    
    # Tüm faturaların kalemlerini topla
    all_items = []
    for invoice in user_invoices:
        items = get_invoice_items_by_invoice(invoice.id)
        all_items.extend(items)
    
    return all_items

@router.get("/phone/{phone_number}/month/{year}/{month}/items", response_model=List[InvoiceItem])
def get_user_invoice_items_by_month_by_phone(phone_number: str, year: int, month: int):
    """Telefon numarasına göre kullanıcının belirli bir aydaki fatura kalemlerini getir"""
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Month must be between 1 and 12")
    
    # Önce telefon numarasından kullanıcıyı bul
    user = get_user_by_phone(phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Ayın ilk ve son günlerini hesapla
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    
    # Belirli dönemdeki faturaları getir
    period_invoices = get_invoices_by_period(start_date, end_date)
    
    # Sadece bu kullanıcının faturalarını filtrele
    user_invoices = [invoice for invoice in period_invoices if invoice.user_id == user.id]
    
    if not user_invoices:
        raise HTTPException(status_code=404, detail=f"No invoices found for this user in {year}/{month}")
    
    # Tüm faturaların kalemlerini topla
    all_items = []
    for invoice in user_invoices:
        items = get_invoice_items_by_invoice(invoice.id)
        all_items.extend(items)
    
    return all_items

@router.get("/user/{user_id}", response_model=List[Invoice])
def get_user_invoices(user_id: int):
    """Kullanıcının faturalarını getir"""
    return get_invoices_by_user(user_id)

@router.get("/phone/{phone_number}/invoices", response_model=List[Invoice])
def get_user_invoices_by_phone(phone_number: str):
    """Telefon numarasına göre kullanıcının faturalarını getir"""
    # Önce telefon numarasından kullanıcıyı bul
    user = get_user_by_phone(phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Kullanıcının faturalarını getir
    return get_invoices_by_user(user.id)

@router.get("/phone/{phone_number}/activeinvoice", response_model=Invoice)
def get_user_active_invoice_by_phone(phone_number: str):
    """Telefon numarasına göre kullanıcının aktif faturasını ve içeriğini getir"""
    user = get_user_by_phone(phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Kullanıcının aktif faturasını getir
    active_invoice = get_active_invoice_by_phone(user.phone_number)
    if not active_invoice:
        raise HTTPException(status_code=404, detail="No active invoice found for this user")
    
    return active_invoice

@router.get("/phone/{phone_number}/activeinvoice/items", response_model=List[InvoiceItem])
def get_user_active_invoice_items_by_phone(phone_number: str):
    """Telefon numarasına göre kullanıcının aktif faturasının kalemlerini getir"""
    user = get_user_by_phone(phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Kullanıcının aktif faturasını getir
    active_invoice = get_active_invoice_by_phone(user.phone_number)
    if not active_invoice:
        raise HTTPException(status_code=404, detail="No active invoice found for this user")
    
    # Aktif faturanın kalemlerini getir
    items = get_invoice_items_by_invoice(active_invoice.id)
    return items

@router.get("/phone/{phone_number}/month/{year}/{month}", response_model=List[Invoice])
def get_user_invoices_by_month_by_phone(phone_number: str, year: int, month: int):
    """Telefon numarasına göre kullanıcının belirli bir aydaki faturalarını getir"""
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Month must be between 1 and 12")
    
    # Önce telefon numarasından kullanıcıyı bul
    user = get_user_by_phone(phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Ayın ilk ve son günlerini hesapla
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    
    # Belirli dönemdeki faturaları getir
    period_invoices = get_invoices_by_period(start_date, end_date)
    
    # Sadece bu kullanıcının faturalarını filtrele
    user_invoices = [invoice for invoice in period_invoices if invoice.user_id == user.id]
    
    return user_invoices

@router.get("/status/{status}", response_model=List[Invoice])
def get_invoices_by_status_route(status: str):
    """Duruma göre faturaları getir (pending, paid, canceled, overdue)"""
    return get_invoices_by_status(status)

@router.get("/unpaid/all", response_model=List[Invoice])
def get_all_unpaid_invoices():
    """Ödenmemiş faturaları getir"""
    return get_unpaid_invoices()

@router.post("/", response_model=Invoice)
def create_new_invoice(invoice: Invoice):
    """Yeni fatura oluştur"""
    return create_invoice(invoice)

@router.put("/{invoice_id}", response_model=Invoice)
def update_invoice_info(invoice_id: int, invoice_data: dict):
    """Fatura bilgilerini güncelle"""
    invoice = update_invoice(invoice_id, invoice_data)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.put("/{invoice_id}/pay")
def mark_as_paid(invoice_id: int):
    """Faturayı ödenmiş olarak işaretle"""
    invoice = mark_invoice_as_paid(invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {"message": "Invoice marked as paid", "invoice_id": invoice.id}

@router.delete("/{invoice_id}")
def delete_invoice_by_id(invoice_id: int):
    """Fatura sil"""
    success = delete_invoice(invoice_id)
    if not success:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {"message": "Invoice deleted successfully"}

@router.get("/period/{start_date}/{end_date}", response_model=List[Invoice])
def get_invoices_by_period_route(start_date: datetime, end_date: datetime):
    """Belirli bir dönemdeki faturaları getir"""
    return get_invoices_by_period(start_date, end_date)

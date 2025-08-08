from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from app.crud.invoice_crud import (
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

@router.get("/user/{user_id}", response_model=List[Invoice])
def get_user_invoices(user_id: int):
    """Kullanıcının faturalarını getir"""
    return get_invoices_by_user(user_id)

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

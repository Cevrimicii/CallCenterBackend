from sqlmodel import Session, select
from typing import List, Optional
from app.models.invoiceitem import InvoiceItem
from app.db.database import engine


def get_invoice_items() -> List[InvoiceItem]:
    """Tüm fatura kalemlerini getir"""
    with Session(engine) as session:
        return session.exec(select(InvoiceItem)).all()


def get_invoice_item_by_id(item_id: int) -> Optional[InvoiceItem]:
    """ID'ye göre fatura kalemi getir"""
    with Session(engine) as session:
        return session.get(InvoiceItem, item_id)


def get_invoice_items_by_invoice(invoice_id: int) -> List[InvoiceItem]:
    """Faturaya göre fatura kalemlerini getir"""
    with Session(engine) as session:
        query = select(InvoiceItem).where(InvoiceItem.invoice_id == invoice_id)
        return session.exec(query).all()


def get_invoice_items_by_service_type(service_type: str) -> List[InvoiceItem]:
    """Hizmet tipine göre fatura kalemlerini getir"""
    with Session(engine) as session:
        query = select(InvoiceItem).where(InvoiceItem.service_type == service_type)
        return session.exec(query).all()


def create_invoice_item(invoice_item: InvoiceItem) -> InvoiceItem:
    """Yeni fatura kalemi oluştur"""
    with Session(engine) as session:
        session.add(invoice_item)
        session.commit()
        session.refresh(invoice_item)
        return invoice_item


def update_invoice_item(item_id: int, item_data: dict) -> Optional[InvoiceItem]:
    """Fatura kalemi bilgilerini güncelle"""
    with Session(engine) as session:
        invoice_item = session.get(InvoiceItem, item_id)
        if invoice_item:
            for key, value in item_data.items():
                setattr(invoice_item, key, value)
            session.add(invoice_item)
            session.commit()
            session.refresh(invoice_item)
            return invoice_item
        return None


def delete_invoice_item(item_id: int) -> bool:
    """Fatura kalemi sil"""
    with Session(engine) as session:
        invoice_item = session.get(InvoiceItem, item_id)
        if invoice_item:
            session.delete(invoice_item)
            session.commit()
            return True
        return False


def calculate_total_for_invoice(invoice_id: int) -> float:
    """Bir faturanın toplam tutarını hesapla"""
    with Session(engine) as session:
        query = select(InvoiceItem).where(InvoiceItem.invoice_id == invoice_id)
        items = session.exec(query).all()
        return sum(item.total_price for item in items)


def create_multiple_invoice_items(invoice_items: List[InvoiceItem]) -> List[InvoiceItem]:
    """Birden fazla fatura kalemi oluştur"""
    with Session(engine) as session:
        for item in invoice_items:
            session.add(item)
        session.commit()
        for item in invoice_items:
            session.refresh(item)
        return invoice_items

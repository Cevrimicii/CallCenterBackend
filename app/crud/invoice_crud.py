from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from app.models.invoice import Invoice
from app.db.database import engine


def get_invoices() -> List[Invoice]:
    """Tüm faturaları getir"""
    with Session(engine) as session:
        return session.exec(select(Invoice)).all()


def get_invoice_by_id(invoice_id: int) -> Optional[Invoice]:
    """ID'ye göre fatura getir"""
    with Session(engine) as session:
        return session.get(Invoice, invoice_id)


def get_invoices_by_user(user_id: int) -> List[Invoice]:
    """Kullanıcıya göre faturaları getir"""
    with Session(engine) as session:
        query = select(Invoice).where(Invoice.user_id == user_id)
        return session.exec(query).all()


def get_invoices_by_status(status: str) -> List[Invoice]:
    """Duruma göre faturaları getir"""
    with Session(engine) as session:
        query = select(Invoice).where(Invoice.status == status)
        return session.exec(query).all()


def get_unpaid_invoices() -> List[Invoice]:
    """Ödenmemiş faturaları getir"""
    with Session(engine) as session:
        query = select(Invoice).where(Invoice.is_paid == False)
        return session.exec(query).all()


def create_invoice(invoice: Invoice) -> Invoice:
    """Yeni fatura oluştur"""
    with Session(engine) as session:
        session.add(invoice)
        session.commit()
        session.refresh(invoice)
        return invoice


def update_invoice(invoice_id: int, invoice_data: dict) -> Optional[Invoice]:
    """Fatura bilgilerini güncelle"""
    with Session(engine) as session:
        invoice = session.get(Invoice, invoice_id)
        if invoice:
            for key, value in invoice_data.items():
                setattr(invoice, key, value)
            session.add(invoice)
            session.commit()
            session.refresh(invoice)
            return invoice
        return None


def delete_invoice(invoice_id: int) -> bool:
    """Fatura sil"""
    with Session(engine) as session:
        invoice = session.get(Invoice, invoice_id)
        if invoice:
            session.delete(invoice)
            session.commit()
            return True
        return False


def mark_invoice_as_paid(invoice_id: int) -> Optional[Invoice]:
    """Faturayı ödenmiş olarak işaretle"""
    with Session(engine) as session:
        invoice = session.get(Invoice, invoice_id)
        if invoice:
            invoice.is_paid = True
            invoice.status = "paid"
            invoice.paid_at = datetime.utcnow()
            session.add(invoice)
            session.commit()
            session.refresh(invoice)
            return invoice
        return None


def get_invoices_by_period(start_date: datetime, end_date: datetime) -> List[Invoice]:
    """Belirli bir dönemdeki faturaları getir"""
    with Session(engine) as session:
        query = select(Invoice).where(
            Invoice.billing_period_start >= start_date,
            Invoice.billing_period_end <= end_date
        )
        return session.exec(query).all()

from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime, timedelta
from app.models.invoice import Invoice
from app.models.invoiceitem import InvoiceItem
from app.models.servicepurchase import ServicePurchase
from app.models.subscription import Subscription
from app.models.package import Package
from app.models.user import User
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

def get_unpaid_invoice(phone_number: str) -> List[Invoice]:
    """Telefon numarasına göre ödenmemiş faturaları getir"""
    with Session(engine) as session:
        query = select(Invoice).join(User).where(
            User.phone_number == phone_number,
            Invoice.is_paid == False
        )
        return session.exec(query).all()

def get_unpaid_invoices() -> List[Invoice]:
    """Ödenmemiş faturaları getir"""
    with Session(engine) as session:
        query = select(Invoice).where(Invoice.is_paid == False)
        return session.exec(query).all()


def get_active_invoice_by_phone(phone_number: str) -> Optional[Invoice]:
    """Telefon numarasına göre aktif faturayı getir (pending veya overdue durumundaki)"""
    with Session(engine) as session:
        query = select(Invoice).join(User).where(
            User.phone_number == phone_number,
        ).order_by(Invoice.created_at.desc())
        return session.exec(query).first()


def create_invoice(invoice: Invoice) -> Invoice:
    """Yeni fatura oluştur - Son 1 ay içindeki hizmet satın alımlarını ve aktif paket ücretini otomatik ekler"""
    with Session(engine) as session:
        # Önce faturayı kaydet
        session.add(invoice)
        session.commit()
        session.refresh(invoice)
        
        # Kullanıcının aktif aboneliğini ve paketini getir
        active_subscription = session.exec(
            select(Subscription).where(
                Subscription.user_id == invoice.user_id,
                Subscription.is_active == True
            )
        ).first()
        
        total_amount = invoice.total_amount or 0
        
        # Aktif paket ücretini faturaya ekle
        if active_subscription:
            package = session.get(Package, active_subscription.package_id)
            if package and package.monthly_fee and package.monthly_fee > 0:
                package_item = InvoiceItem(
                    invoice_id=invoice.id,
                    service_type="Package",
                    description=f"Aylık Paket Ücreti - {package.name}",
                    quantity=1,
                    unit_price=package.monthly_fee,
                    total_price=package.monthly_fee,
                    tax_rate=0.18  # %18 KDV
                )
                
                session.add(package_item)
                total_amount += package.monthly_fee
        
        # Son 1 ay içindeki hizmet satın alımlarını getir
        one_month_ago = invoice.created_at - timedelta(days=30)
        
        service_purchases = session.exec(
            select(ServicePurchase).where(
                ServicePurchase.user_id == invoice.user_id,
                ServicePurchase.purchase_date >= one_month_ago,
                ServicePurchase.purchase_date <= invoice.created_at,
                ServicePurchase.is_used == False  # Henüz faturaya eklenmemiş olanlar
            )
        ).all()
        
        # Her hizmet satın alımını fatura kalemi olarak ekle
        for purchase in service_purchases:
            invoice_item = InvoiceItem(
                invoice_id=invoice.id,
                service_type=purchase.service_type,
                description=f"{purchase.service_type} - {purchase.count} adet",
                quantity=purchase.count,
                unit_price=purchase.unit_price,
                total_price=purchase.purchase_price,
                tax_rate=0.18  # %18 KDV
            )
            
            session.add(invoice_item)
            total_amount += purchase.purchase_price
            
            # Hizmet satın alımını kullanılmış olarak işaretle
            purchase.is_used = True
            session.add(purchase)
        
        # Faturanın toplam tutarını güncelle
        invoice.total_amount = total_amount
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

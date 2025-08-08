from sqlmodel import create_engine, SQLModel
from app.db.config import get_settings

from app.models.user import User
from app.models.package import Package
from app.models.subscription import Subscription
from app.models.invoice import Invoice
from app.models.invoiceitem import InvoiceItem
from app.models.remaininguses import RemainingUses
from app.models.agentintentlog import AgentIntentLog
from app.models.packagechangerequest import PackageChangeRequest
from app.models.problems import Problem
from app.models.servicepurchase import ServicePurchase

settings = get_settings()
engine = create_engine(settings.database_url, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)
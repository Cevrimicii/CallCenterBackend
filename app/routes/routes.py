from fastapi import APIRouter

from .user_routes import router as user_router
from .package_routes import router as package_router
from .subscription_routes import router as subs_router
from .invoice_routes import router as invoice_router
from .problem_routes import router as problem_router
from .remaining_uses_routes import router as remaining_uses_router
from .service_purchase_routes import router as service_purchase_router
from .agent_intent_log_routes import router as agent_log_router
from .package_change_request_routes import router as package_request_router
from .dashboard_routes import router as dashboard_router
from .customer_service_routes import router as customer_service_router

router = APIRouter()

api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(package_router)
api_router.include_router(subs_router)
api_router.include_router(invoice_router)
api_router.include_router(problem_router)
api_router.include_router(remaining_uses_router)
api_router.include_router(service_purchase_router)
api_router.include_router(agent_log_router)
api_router.include_router(package_request_router)
api_router.include_router(dashboard_router)
api_router.include_router(customer_service_router)


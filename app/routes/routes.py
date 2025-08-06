from fastapi import APIRouter
from app.db.database import init_db
from app.crud import getUsers, create_user,get_package_by_user, get_packages
from app.models.package import Package
from app.models.user import User
from .user_routes import router as user_router
from .package_routes import router as package_router

router = APIRouter()

api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(package_router)


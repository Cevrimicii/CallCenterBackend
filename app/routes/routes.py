from fastapi import APIRouter
from app.db.database import init_db
from app.crud import getUsers, create_user,get_package_by_user, get_packages
from app.models.package import Package
from app.models.user import User

router = APIRouter()

@router.on_event("startup")
def on_startup():
    init_db()

@router.get("/users", response_model=list[User])
def get_users():
    return getUsers()

@router.post("/users", response_model=User)
def add_user(user: User):
    return create_user(user)

@router.get("/packages", response_model=list[Package])
def get_packagelist():
    return get_packages()

@router.get("/package", response_model=Package)
def getPackageByUser(phoneNumber: str):
    return get_package_by_user(phoneNumber)

@router.post("/package", response_model=Package)
def add_user(package: Package):
    return create_user(package)
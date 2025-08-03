from sqlmodel import Session, select
from app.models.package import Package
from app.models.user import User
from app.db.database import engine

def getUsers():
    with Session(engine) as session:
        return session.exec(select(User)).all()
    
def get_packages():
    with Session(engine) as session:
        return session.exec(select(Package)).all()

def get_package_by_user(phoneNumber: str):
    with Session(engine) as session:
        query = select(User).where(User.phone_number == phoneNumber)
        user = session.exec(query).first()
        if user is not None:
            statement = select(Package).where(Package.id == user.package_id)
            result = session.exec(statement).first()
            return result
        else:
            return None
        

def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    
def create_package(package: Package):
    with Session(engine) as session:
        session.add(package)
        session.commit()
        session.refresh(package)
        return package
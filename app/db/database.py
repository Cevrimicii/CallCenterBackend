from sqlmodel import create_engine, SQLModel
from app.db.config import get_settings

settings = get_settings()
engine = create_engine(settings.database_url, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)
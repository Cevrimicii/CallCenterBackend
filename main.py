from fastapi import FastAPI
from app.routes.routes import api_router
from app.db.database import init_db

init_db()

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")

# if __name__ == '__main__':
#      uvicorn.run(app, host='0.0.0.0', port=8000)
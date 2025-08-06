from fastapi import FastAPI
from app.routes import routes
import uvicorn

app = FastAPI()

app.include_router(routes.router)

# if __name__ == '__main__':
#      uvicorn.run(app, host='0.0.0.0', port=8000)
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from app.routes.routes import api_router
from app.db.database import init_db
from app.utils.logging_config import setup_logging, get_logger, log_api_request
from app.middleware.error_handler import error_handling_middleware
import time
import logging

# Logging sistemini başlat
setup_logging()
logger = get_logger('app.main')

# Veritabanını başlat
init_db()
logger.info("Database initialized successfully")

app = FastAPI(
    title="Call Center Backend API",
    description="Call Center Management System Backend API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da specific origin'ler kullanın
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Request bilgilerini logla
    client_ip = request.client.host if request.client else "unknown"
    log_api_request(
        method=request.method,
        path=str(request.url.path),
        ip=client_ip
    )
    
    # Error handling ile response'u işle
    response = await error_handling_middleware(request, call_next)
    
    # İşlem süresini hesapla
    process_time = time.time() - start_time
    
    # Response bilgilerini logla
    logger.info(
        f"Request completed: {request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.3f}s - "
        f"IP: {client_ip}"
    )
    
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Router'ı ekle
app.include_router(api_router, prefix="/api/v1")

# Health check endpoint
@app.get("/health")
async def health_check():
    logger.info("Health check requested")
    return {"status": "healthy", "message": "Call Center Backend API is running"}

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Application startup completed")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown initiated")

# if __name__ == '__main__':
#      uvicorn.run(app, host='0.0.0.0', port=8000)
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import traceback
from app.utils.logging_config import get_logger, log_error
import json

logger = get_logger('app.middleware.error')

async def error_handling_middleware(request: Request, call_next):
    """Global error handling middleware"""
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        # Hatayı logla
        log_error(e, f"Unhandled error in {request.method} {request.url.path}")
        
        # Client IP'sini al
        client_ip = request.client.host if request.client else "unknown"
        
        # Detaylı hata logu
        logger.error(
            f"Unhandled error: {str(e)} - "
            f"Method: {request.method} - "
            f"Path: {request.url.path} - "
            f"IP: {client_ip} - "
            f"Query Params: {dict(request.query_params)}"
        )
        
        # Development modunda stack trace'i de logla
        logger.error(f"Stack trace: {traceback.format_exc()}")
        
        # Generic error response döndür
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "error_id": str(hash(str(e)))  # Hata takibi için unique ID
            }
        )

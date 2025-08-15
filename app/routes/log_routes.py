from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from datetime import datetime, timedelta
import os
from pathlib import Path
from app.utils.logging_config import get_logger

router = APIRouter(
    prefix="/logs",
    tags=["logs"],
    responses={404: {"description": "Not found"}},
)

logger = get_logger('app.routes.logs')

@router.get("/health")
async def get_logging_health():
    """Logging sisteminin durumunu kontrol et"""
    log_dir = Path("logs")
    
    if not log_dir.exists():
        raise HTTPException(status_code=500, detail="Log directory not found")
    
    log_files = list(log_dir.glob("*.log"))
    
    health_info = {
        "status": "healthy",
        "log_directory": str(log_dir.absolute()),
        "log_files_count": len(log_files),
        "log_files": [f.name for f in log_files],
        "total_log_size_mb": sum(f.stat().st_size for f in log_files) / (1024 * 1024)
    }
    
    logger.info("Logging health check requested")
    return health_info

@router.get("/recent-errors")
async def get_recent_errors(limit: int = Query(50, ge=1, le=1000)):
    """Son hataları getir"""
    try:
        log_dir = Path("logs")
        today = datetime.now().strftime("%Y-%m-%d")
        error_log_file = log_dir / f"error_{today}.log"
        
        if not error_log_file.exists():
            return {"errors": [], "message": "No error log file found for today"}
        
        # Son N satırı oku
        with open(error_log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        recent_lines = lines[-limit:] if len(lines) > limit else lines
        
        return {
            "errors": [line.strip() for line in recent_lines],
            "total_lines": len(recent_lines),
            "file": str(error_log_file)
        }
        
    except Exception as e:
        logger.error(f"Error reading error logs: {str(e)}")
        raise HTTPException(status_code=500, detail="Error reading error logs")

@router.get("/stats")
async def get_log_stats():
    """Log istatistikleri"""
    try:
        log_dir = Path("logs")
        today = datetime.now().strftime("%Y-%m-%d")
        
        stats = {
            "date": today,
            "files": {}
        }
        
        # Her log dosyası için istatistik
        for log_type in ["app", "error", "access"]:
            log_file = log_dir / f"{log_type}_{today}.log"
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                stats["files"][log_type] = {
                    "total_lines": len(lines),
                    "file_size_mb": log_file.stat().st_size / (1024 * 1024),
                    "last_modified": datetime.fromtimestamp(log_file.stat().st_mtime).isoformat()
                }
            else:
                stats["files"][log_type] = {
                    "total_lines": 0,
                    "file_size_mb": 0,
                    "last_modified": None
                }
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting log stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Error getting log stats")

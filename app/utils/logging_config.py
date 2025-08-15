import logging
import logging.config
import os
from datetime import datetime
from pathlib import Path


# Log dizinini oluştur
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Log dosyası adları
current_date = datetime.now().strftime("%Y-%m-%d")
APP_LOG_FILE = LOG_DIR / f"app_{current_date}.log"
ERROR_LOG_FILE = LOG_DIR / f"error_{current_date}.log"
ACCESS_LOG_FILE = LOG_DIR / f"access_{current_date}.log"

# Logging konfigürasyonu
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s:%(lineno)d - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(asctime)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'json': {
            'format': '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "module": "%(module)s", "function": "%(funcName)s", "line": %(lineno)d, "message": "%(message)s"}',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout'
        },
        'file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': str(APP_LOG_FILE),
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'encoding': 'utf8'
        },
        'error_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'detailed',
            'filename': str(ERROR_LOG_FILE),
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'encoding': 'utf8'
        },
        'access_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'json',
            'filename': str(ACCESS_LOG_FILE),
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'encoding': 'utf8'
        }
    },
    'loggers': {
        '': {  # Root logger
            'handlers': ['console', 'file_handler', 'error_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
        'app': {
            'handlers': ['console', 'file_handler', 'error_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
        'access': {
            'handlers': ['access_handler'],
            'level': 'INFO',
            'propagate': False
        },
        'uvicorn.error': {
            'handlers': ['console', 'file_handler'],
            'level': 'INFO',
            'propagate': False
        },
        'uvicorn.access': {
            'handlers': ['access_handler'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

def setup_logging():
    """Logging sistemini başlat"""
    logging.config.dictConfig(LOGGING_CONFIG)
    
def get_logger(name: str = None):
    """Logger instance'ı al"""
    if name is None:
        name = 'app'
    return logging.getLogger(name)

# Özel log fonksiyonları
def log_database_operation(operation: str, table: str, record_id: int = None, details: str = None):
    """Veritabanı operasyonlarını logla"""
    logger = get_logger('app.database')
    message = f"Database {operation} on {table}"
    if record_id:
        message += f" (ID: {record_id})"
    if details:
        message += f" - {details}"
    logger.info(message)

def log_api_request(method: str, path: str, user_id: int = None, ip: str = None):
    """API isteklerini logla"""
    logger = get_logger('access')
    message = f"API {method} {path}"
    if user_id:
        message += f" - User: {user_id}"
    if ip:
        message += f" - IP: {ip}"
    logger.info(message)

def log_error(error: Exception, context: str = None):
    """Hataları logla"""
    logger = get_logger('app.error')
    message = f"Error: {str(error)}"
    if context:
        message = f"{context} - {message}"
    logger.error(message, exc_info=True)

def log_business_operation(operation: str, details: str, user_id: int = None):
    """İş operasyonlarını logla"""
    logger = get_logger('app.business')
    message = f"Business Operation: {operation} - {details}"
    if user_id:
        message += f" (User: {user_id})"
    logger.info(message)

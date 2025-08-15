import functools
import time
from typing import Any, Callable
from app.utils.logging_config import get_logger

logger = get_logger('app.utils.decorators')

def log_execution_time(func_name: str = None):
    """Fonksiyon çalışma süresini loglar"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            name = func_name or f"{func.__module__}.{func.__name__}"
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                logger.info(f"Function {name} executed successfully in {execution_time:.3f}s")
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"Function {name} failed after {execution_time:.3f}s - Error: {str(e)}")
                raise
                
        return wrapper
    return decorator

def log_database_query(operation: str, table: str):
    """Database sorgu operasyonlarını loglar"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # Result sayısını belirlemeye çalış
                count = "N/A"
                if isinstance(result, list):
                    count = len(result)
                elif result is not None:
                    count = 1
                else:
                    count = 0
                    
                logger.info(f"DB {operation} on {table} - Records: {count} - Time: {execution_time:.3f}s")
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"DB {operation} on {table} failed after {execution_time:.3f}s - Error: {str(e)}")
                raise
                
        return wrapper
    return decorator

def log_api_endpoint(endpoint_name: str = None):
    """API endpoint'lerini loglar"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            name = endpoint_name or func.__name__
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                logger.info(f"API endpoint {name} completed successfully in {execution_time:.3f}s")
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"API endpoint {name} failed after {execution_time:.3f}s - Error: {str(e)}")
                raise
                
        return wrapper
    return decorator

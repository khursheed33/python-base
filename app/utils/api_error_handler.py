import logging
from functools import wraps
from fastapi import HTTPException
from app.models.all_models import ResponseModel

class CatchAPIException:
    def __init__(self) -> None:
        logging.basicConfig(filename='logs/api-logs.log', level=logging.ERROR)    

    def catch_api_exceptions(self,func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except HTTPException as e:
                # Log the error
                logging.error(str(e))
                # Handle different HTTP status codes
                if e.status_code == 403:
                    return ResponseModel(message="Forbidden",error='Forbidden', status='failed', status_code=403), 403
                elif e.status_code == 404:
                    return ResponseModel(message="Not Found",error='Not Found', status='failed', status_code=404), 404
                # Add more status codes as needed
                else:
                    return ResponseModel(message=e.detail,error=e.detail, status='failed', status_code=e.status_code), e.status_code
            except Exception as e:
                # Log the error
                logging.error(str(e))
                # For all other exceptions, return a 500 Internal Server Error
                error_message = str(e)
                return ResponseModel(message=error_message,error=error_message, status='failed', status_code=500),500

        return wrapper

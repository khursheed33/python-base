import logging
from functools import wraps
from fastapi import HTTPException


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
                    return {"error": "Forbidden"}, 403
                elif e.status_code == 404:
                    return {"error": "Not Found"}, 404
                # Add more status codes as needed
                else:
                    return {"error": str(e.detail)}, e.status_code
            except Exception as e:
                # Log the error
                logging.error(str(e))
                # For all other exceptions, return a 500 Internal Server Error
                error_message = str(e)
                return {"error": error_message}, 500

        return wrapper

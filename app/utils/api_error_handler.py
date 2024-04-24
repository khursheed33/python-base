import logging
from functools import wraps
from fastapi import HTTPException
from fastapi.responses import JSONResponse
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
                response_model = ResponseModel(
                    message=e.detail,
                    error=e.detail,
                    status=ResponseModel.FAILED,
                    status_code=e.status_code
                )
                return JSONResponse(content=response_model.model_dump(), status_code=e.status_code)

            except Exception as e:
                # Log the error
                logging.error(str(e))
                # For all other exceptions, return a 500 Internal Server Error
                error_message = str(e)
                response_model = ResponseModel(
                    message=error_message,
                    error=str(e),
                    status=ResponseModel.FAILED,
                    status_code=ResponseModel.INTERNAL_SERVER_ERROR_500
                )
                return JSONResponse(content=response_model.model_dump(), status_code=500)

        return wrapper

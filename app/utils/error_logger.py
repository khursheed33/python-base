import logging
import functools

def error_logging(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except Exception as e:
            logging.exception("An error occurred: %s", str(e))
            return {"error": "An unexpected error occurred"}, 500
    return wrapper

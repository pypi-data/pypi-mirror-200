from loguru import logger
import functools
import time




#logger.add("app.log", rotation="500 MB", compression="zip")

def logexc(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Starting function {func.__name__}")
        logger.info(f"Arguments: {args}, {kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"Result: {result}")
        except Exception as e:
            logger.error(f"<{e.__class__.__name__}>: Error in {func.__name__}: {e}")
            raise
        else:
            logger.info(f"Finished function {func.__name__}")
            return result

    return wrapper

def logtime(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"Function {func.__name__} took {elapsed_time:.6f} seconds to execute.")
        return result
    return wrapper

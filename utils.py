import time
from  logger import logger

def retry(function, max_attempts=3, delay=1, *args, **kwargs):
    """
    Retry a function a specified number of times with a delay between attempts.
    
    :param function: The function to be invoked.
    :param max_attempts: The maximum number of retry attempts.
    :param delay: The delay (in seconds) between retry attempts.
    :param args: Positional arguments to pass to the function.
    :param kwargs: Keyword arguments to pass to the function.
    :return: The result of the function if successful, otherwise None.
    """
    for attempt in range(1, max_attempts + 1):
        try:
            result = function(*args, **kwargs)
            return result  # If successful, return the result
        except Exception as e:
            if attempt < max_attempts:
                logger.error(f"Attempt {attempt} failed. Got Exception {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logger.error(f"Maximum retry attempts reached. Failed: {e}")
    return None  # If all retry attempts fail, return None

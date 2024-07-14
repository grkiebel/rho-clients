import requests
from logging import Logger
from pydantic import BaseModel
from typing import Dict, List


base_url = None
logger = None


def initialize(url: str, lgr: Logger):
    global base_url
    global logger
    base_url = url
    logger = lgr


def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.HTTPError as e:
            logger.error(f"HTTP Error: {e}")
            return None
        except requests.ConnectionError as e:
            logger.error(f"Connection Error: {e}")
            return None
        except requests.Timeout as e:
            logger.error(f"Timeout Error: {e}")
            return None
        except requests.RequestException as e:
            logger.error(f"Request Error: {e}")
            return None

    return wrapper

import logging


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    c_handler = logging.StreamHandler()
    c_format = logging.Formatter("%(asctime)s : %(name)s - %(levelname)s - %(message)s")
    c_handler.setFormatter(c_format)
    logger.addHandler(c_handler)
    return logger


if __name__ == "__main__":
    logger = get_logger("BoB")
    logger.info("Testing log_config")

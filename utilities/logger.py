import logging
from logging.handlers import RotatingFileHandler
from config import settings

LOG_FILE = "/var/log/app_log/app.log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s"

handlers = [
    # logging.FileHandler(LOG_FILE),  # Log to file
    logging.StreamHandler()  # Log to console
]

# 300 MB in bytes
MAX_LOG_SIZE = 300 * 1024 * 1024
MAX_DAYS = 7

if not settings.DEVELOPMENT:
    log_rotate_handler = RotatingFileHandler(
        filename=LOG_FILE,
        maxBytes=MAX_LOG_SIZE,  # Rotate when file size exceeds 300 MB
        # when="D",  # Rotate daily
        # interval=1,  # Rotate every day
        backupCount=MAX_DAYS  # Keep logs for 1 day
    )
    formatter = logging.Formatter(LOG_FORMAT)
    log_rotate_handler.setFormatter(formatter)

    handlers.append(log_rotate_handler)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=handlers
)

def get_logger(name):
    return logging.getLogger(name)
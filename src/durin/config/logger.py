import logging
import os

# Global logger configuration
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(module)s.%(funcName)s [line %(lineno)d] - %(message)s",
    handlers=[logging.StreamHandler()]
)

# Get the main logger
logger = logging.getLogger("durin")

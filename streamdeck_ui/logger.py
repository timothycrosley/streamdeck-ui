import logging
import sys

from streamdeck_ui.config import LOG_FILE

logger = logging.getLogger("streamdeck_ui")
stderr_handler = logging.StreamHandler(sys.stderr)
file_handler = logging.FileHandler(LOG_FILE)
logger.addHandler(stderr_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

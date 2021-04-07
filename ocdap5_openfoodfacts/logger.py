import logging

LEVEL = logging.INFO

LOG_FORMAT = "%(asctime)s %(levelname)s:  %(message)s"
logging.basicConfig(level=LEVEL,
                    format=LOG_FORMAT)
logger = logging.getLogger()

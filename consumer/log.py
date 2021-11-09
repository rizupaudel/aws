import logging
# Logging format
LOG_FILE = 'consumer.log'
LOG_FORMAT = '%(asctime)s %(filename)s: %(levelname)s: %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
HANDLERS = [logging.FileHandler(LOG_FILE) , logging.StreamHandler()]

logging.basicConfig(format=LOG_FORMAT, 
                    datefmt=DATE_FORMAT, 
                    level=logging.INFO,
                    handlers=HANDLERS)

log = logging.getLogger(__name__)
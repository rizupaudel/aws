import logging
# Logging format
LOG_FILE = 'consumer.log'
LOG_FORMAT = '%(asctime)s %(filename)s: %(levelname)s: %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, datefmt=DATE_FORMAT, level=logging.INFO)

log = logging.getLogger(__name__)
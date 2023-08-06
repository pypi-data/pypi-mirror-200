import logging as log
from devgoldyutils import add_custom_handler

logger = add_custom_handler(log.getLogger("uwu"), level=log.DEBUG)

logger.debug("jeff")
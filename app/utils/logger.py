import logging
from logging.handlers import TimedRotatingFileHandler
import os

def setup_logger(name="logger", log_file="logs/my_project.log", level=logging.INFO):
    """Set up logger with timed file rotation."""
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
    
    # Create logs directory if it does not exist
    if not os.path.exists('./logs'):
        os.makedirs('./logs')

    handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=7) 
    handler.setFormatter(formatter)
    handler.setLevel(level)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    logger.propagate = False

    return logger

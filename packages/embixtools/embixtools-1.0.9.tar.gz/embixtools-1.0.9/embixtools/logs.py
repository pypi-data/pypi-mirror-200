import sys
import os
from datetime import datetime
from pytz import timezone, utc
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup(
    level = 'info', 
    format = '%(asctime)s - %(levelname)s - %(message)s'
):
    lvl = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }[level]
    logger = logging.getLogger()
    logger.setLevel(lvl)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(lvl)
    def customTime(*args):
        utc_dt = utc.localize(datetime.utcnow())
        my_tz = timezone('Europe/Paris')
        converted = utc_dt.astimezone(my_tz)
        return converted.timetuple()
    logging.Formatter.converter = customTime    
    handler.setFormatter(logging.Formatter(format))
    logger.addHandler(handler)

def reset(): 
    logger = logging.getLogger()
    for h in logger.handlers:
        logger.removeHandler(h)
    logging.basicConfig(level=logging.WARNING)
import configparser
import logging
import sys
import ssl
import asyncio
from logging.handlers import RotatingFileHandler
from pathlib import Path
import uvloop
from app.config import settings

THIS_FOLDER = Path(__file__).parent.resolve()

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

SSL_CONTEXT = ssl.create_default_context()

conf_file = THIS_FOLDER / "conf.ini"
log_file = THIS_FOLDER / "logs/mainlog.log"

config = configparser.ConfigParser()
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

config.read(conf_file)

rootLogger=logging.getLogger('AppLogger')
rootLogger.setLevel(logging.DEBUG)

consholeHandler=logging.StreamHandler(stream=sys.stdout)
consholeHandler.setFormatter(logFormatter)
rootLogger.addHandler(consholeHandler)

if settings.log2file is True:
  fileHandler = RotatingFileHandler(log_file,maxBytes=25000, backupCount=7)
  fileHandler.setFormatter(logFormatter)
  rootLogger.addHandler(fileHandler)

sysLogHandler = logging.handlers.SysLogHandler(address = '/dev/log')
sysLogHandler.setFormatter(logFormatter)
rootLogger.addHandler(sysLogHandler)

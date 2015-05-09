import logging
from dbLogHandler import dbLogHandler
import datetime
import dbagent

def setupLog(loglevel):
    numeric_level = getattr(logging, loglevel.upper(), None)

    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    #setup file logger
    now = datetime.datetime.utcnow()
    log_file_name = now.strftime('%Y%m%d')

    fileh = logging.FileHandler('log/%s.log' % log_file_name, 'a')
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')
    fileh.setFormatter(formatter)

    #setup db logger
    dbh = dbLogHandler()

    log = logging.getLogger()  # root logger
    for hdlr in log.handlers:  # remove all old handlers
        log.removeHandler(hdlr)

    log.addHandler(fileh)      # set the new handler
    log.addHandler(dbh)      # set the new handler

    log.setLevel(numeric_level)
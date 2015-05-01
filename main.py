from scraper import *
import time
import datetime
import logging
while 1:

    #log file setup
    loglevel = arg[1]
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    now = datetime.datetime.utcnow()
    log_file_name = now.strftime('%Y%m%d')

    fileh = logging.FileHandler('log/%s.log' % log_file_name, 'a')
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')
    fileh.setFormatter(formatter)

    log = logging.getLogger()  # root logger
    for hdlr in log.handlers:  # remove all old handlers
        log.removeHandler(hdlr)
    log.addHandler(fileh)      # set the new handler
    log.setLevel(numeric_level)

    #scrape

    logging.info('Scraper(%d) started scraping', 1)
    s = backpackers_com_tw.Scraper()
    s.scrape()
    logging.info('Scraper(%d) stopped scraping', 1)

    logging.info('Scraper(%d) started scraping', 2)
    s = facebook_com.Scraper()
    s.scrape()
    logging.info('Scraper(%d) stopped scraping', 2)

    time.sleep(3*60)
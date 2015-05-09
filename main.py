from scraper import *
import time
import logger
import sys
import dbagent
import logging

while 1:

    #log file setup
    loglevel = sys.argv[1]
    logger.setupLog(loglevel)

    #create a new run
    run_id = dbagent.add_run()
    sources = dbagent.get_sources()
    source_ids = [src['id'] for src in sources]
    dbagent.prepare_all_scrape(run_id, source_ids)

    #scrape
    logging.info('Scraper(%d) started scraping', 1)
    s = backpackers_com_tw.Scraper()
    s.scrape(run_id)
    logging.info('Scraper(%d) stopped scraping', 1)

    logging.info('Scraper(%d) started scraping', 2)
    s = facebook_com.Scraper()
    s.scrape(run_id)
    logging.info('Scraper(%d) stopped scraping', 2)

    time.sleep(3*60)
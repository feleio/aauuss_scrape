import logging
import dbagent

class dbLogHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def flush(self):
        pass

    def emit(self, record):
        try:
            msg = self.format(record)
            scrape_id = getattr(record, 'scrape_id', 0)
            dbagent.add_log(scrape_id, msg)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


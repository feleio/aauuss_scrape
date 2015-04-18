import codecs
from datetime import datetime

log_file_name = 'log/scrapper.log'

def log(log_type, str):
	with codecs.open(log_file_name, 'a', encoding='utf8') as log:
		now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		log.write("%s [%s] %s\n" % (now_str, log_type, str))
		
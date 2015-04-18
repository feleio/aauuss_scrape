import MySQLdb
from datetime import datetime

import logger
import socket

if(socket.gethostname() == "homestead"):
	db = MySQLdb.connect(	host='localhost',
							port=33060,
							user='homestead',
							passwd='secret',
							db='aauuss',
							charset='utf8',
							use_unicode=True)
else:
	db = MySQLdb.connect(	host='localhost',
							user='root',
							passwd='zxadzxad',
							db='aauuss',
							charset='utf8',
							use_unicode=True)
cursor = db.cursor()

def set_time_zone(time_zone_str):
	global db
	db.time_zone = time_zone_str

def is_post_exist(src_id, remote_id):
	global cursor
	sql = "SELECT EXISTS( SELECT 1 FROM posts WHERE source_id = %s AND remote_id = %s)"
	cursor.execute(sql, (src_id, remote_id))
	return cursor.fetchone()[0]
	
def add_post(title, content, url, author, sourceId, remote_id, postedAt, ):
	global cursor
	values = (	unicode(title), 
				unicode(content), 
				unicode(url), 
				unicode(author),
				sourceId, 
				remote_id,
				postedAt.strftime('%Y-%m-%d %H:%M:%S'))
	sql = 	u"INSERT INTO posts (title,content,url,author,source_id,remote_id,posted_at,created_at,updated_at) "\
			"VALUES (%s,%s,%s,%s,%s,%s,%s,now(),now())"

	try:
		cursor.execute(sql, values)
		db.commit()
		return cursor.lastrowid
	except:
		db.rollback()
		raise


def get_sources(scraper_id):
	global cursor
	sql = "SELECT id, url FROM sources WHERE scraper_id = %d" % scraper_id
	cursor.execute(sql)
	results = cursor.fetchall()
	return [{'id':src[0],'url':src[1]} for src in results]

def get_latest_time(source_id):
	global cursor
	sql = 	"SELECT posted_at FROM posts WHERE source_id = %d "\
			"ORDER BY posted_at DESC LIMIT 1" % source_id
	cursor.execute(sql)
	result = cursor.fetchone()
	if result and len(result) > 0:
		return result[0]
	else:
		return None

def add_post_tag(post_id, tag_id):
	global cursor
	values = (post_id, tag_id)
	sql = 	u"INSERT INTO post_tag (post_id,tag_id) "\
			"VALUES (%d,%d)" % values

	try:
		cursor.execute(sql)
		db.commit()
		return True
	except:
		db.rollback()
		return False

def get_source_tags(source_id):
	global cursor
	sql = "SELECT tag_id FROM source_tag WHERE source_id = %d" % source_id
	cursor.execute(sql)
	results = cursor.fetchall()
	return [src[0] for src in results]
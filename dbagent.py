import MySQLdb
from datetime import datetime

db = MySQLdb.connect(	host='localhost',
						port=33060,
						user='homestead',
						passwd='secret',
						db='aauuss',
						charset='utf8')
cursor = db.cursor()

def set_time_zone(time_zone_str):
	global db
	db.time_zone = time_zone_str

def is_post_exist(postTitle, author=None):
	global cursor
	if author != None:
		sql = "SELECT EXISTS( SELECT 1  FROM posts WHERE title = '%s' AND author = '%s')" % (postTitle, author)
	else:
		sql = "SELECT EXISTS( SELECT 1  FROM posts WHERE title = '%s')" % postTitle
	cursor.execute(sql)
	return cursor.fetchone()[0]

def add_post(title, content, url, author, sourceId, postedAt ):
	global cursor
	values = (title, content, url, author, sourceId, postedAt.strftime('%Y-%m-%d %H:%M:%S'))
	sql = 	u"INSERT INTO posts (title,content,url,author,source_id,posted_at,created_at,updated_at) "\
			"VALUES ('%s','%s','%s','%s',%d,'%s',now(),now())" % values

	try:
		cursor.execute(sql)
		db.commit()
		return True
	except:
		db.rollback()
		return False

def add_post(title, content, url, author, sourceId, postedAt ):
	global cursor
	values = (title, content, url, author, sourceId, postedAt.strftime('%Y-%m-%d %H:%M:%S'))
	sql = 	u"INSERT INTO posts (title,content,url,author,source_id,posted_at,created_at,updated_at) "\
			"VALUES ('%s','%s','%s','%s',%d,'%s',now(),now())" % values

	try:
		cursor.execute(sql)
		db.commit()
		return True
	except:
		db.rollback()
		return False


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


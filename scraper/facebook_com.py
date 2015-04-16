# -*- coding: utf-8 -*-
import re
import simplejson

from datetime import datetime

#my modules
import dbagent
import url
import logger

class Scraper:
	def __init__(self):
		self._scraper_id = 2
		self._token = "CAALN1209ZAmgBAMpVBq7m8yDo7hj5ThZCZC67IVUUoq1ZBOoOOe4MNETUD1w38uNDzUzZCu2nTfKu87rLwPwRVgwNrtl7hZC6O5VFvv622PWDxeiEOl73p5TujuyvWzKo3bYRCnTZAnIW0PWZBGmi2Oc79S2xvinKJBfcNFZBKzMuBn5hvTROMUDl"
		dbagent.set_time_zone('+00:00')

	def _scrape(self, src_id, src_remote_id):
		src_url = ("https://graph.facebook.com/v2.3/%s/feed?access_token=%s" 
				% (src_remote_id, self._token))

		scape_count = 0
		json = simplejson.load(url.get(src_url))

		for post in json['data']:
		    remote_id = post['id']
		    if(not dbagent.is_post_exist(src_id, remote_id)):
			    if('message' in post):
			        splits = post['message'].split('\n',1)
			        title = splits[0]
			        content = splits[1] if (len(splits) > 1) else ''
			    elif('description' in post):
			        splits = post['description'].split('\n',1)
			        title = splits[0]
			        content = splits[1] if (len(splits) > 1) else ''
			    else:
			        title = ''
			        content = ''
			    title = title[:30] if (len(title) > 30) else title
			    
			    link = "https://www.facebook.com/"+post['id']
			    author = post['from']['name']
			    posted_at = datetime.strptime(post['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
			    new_post_id = dbagent.add_post(title, content, link, author, src_id, remote_id, posted_at)
			    self._add_tags(src_id, new_post_id)
			    scape_count += 1

		logger.log(	'info', 'scraper(%d), src(%d): %d posts saved' 
					% (self._scraper_id, src_id, scape_count))

	# def _get_post_id(self, url):
	# 	prog = re.compile('^.+=(\d+)$')
	# 	result = prog.match(url)
	# 	return result.group(1)

	def _add_tags(self, source_id, post_id):
		for tag_id in dbagent.get_source_tags(source_id):
			dbagent.add_post_tag(post_id, tag_id)

	def scrape(self):
		for src in dbagent.get_sources(self._scraper_id):
			self._scrape(src['id'], src['url'])

		#self._scrape(27, 'http://www.backpackers.com.tw/forum/external.php?type=RSS2&amp;forumids=309')
		
		#print(self._sources())
		#for src in self._sources():
		#	self._scrape(src)
		
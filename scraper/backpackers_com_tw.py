# -*- coding: utf-8 -*-
import re
import logger

from bs4 import BeautifulSoup
from datetime import datetime

#my modules
import dbagent
import url

class Scraper:
	def __init__(self):
		self._scraper_id = 1
		dbagent.set_time_zone('+00:00')

	def _scrape(self, src_id, src_url):
		xml_doc = url.get(src_url)
		soup = BeautifulSoup(xml_doc, "xml")

		latest = dbagent.get_latest_time(src_id)
		post_id = self._get_post_id(src_url)

		scape_count = 0

		for item in soup('item'):
			pub_date = item.pubDate.string
			postedAt = datetime.strptime(pub_date,'%a, %d %b %Y %H:%M:%S GMT')

			link_post_id = self._get_post_id(item.category['domain'])

			if latest == None or latest < postedAt:
				if post_id == link_post_id:
					title = item.title.string
					link = item.link.string
					content = item.description.string
					author = ''

					dbagent.add_post(title, content, link, author, src_id, postedAt)
					scape_count += 1
			else:
				break

		logger.log(	'info', 'scraper(%d), src(%d): %d posts saved' 
					% (self._scraper_id, src_id, scape_count))

	def _get_post_id(self, url):
		prog = re.compile('^.+=(\d+)$')
		result = prog.match(url)
		return result.group(1)


	def scrape(self):
		for src in dbagent.get_sources(self._scraper_id):
			self._scrape(src['id'], src['url'])
		#print(self._sources())
		#for src in self._sources():
		#	self._scrape(src)
		
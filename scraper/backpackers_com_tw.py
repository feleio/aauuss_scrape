# -*- coding: utf-8 -*-
import re
import logging
import traceback

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
        try:
            xml_doc = url.get(src_url).read().decode('utf-8','ignore')
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
                        try:
                            title = item.title.string
                            link = item.link.string
                            content = item.description.string
                            author = ''
                            remote_id = 0
                            #print ('scraper(%d), src(%d): id: %s' % (self._scraper_id, src_id, self._get_post_id(link)))
                            new_post_id = dbagent.add_post(title, content, link, author, src_id, remote_id, postedAt)
                            self._add_tags(src_id, new_post_id)
                            scape_count += 1
                        except Exception, err:
                            logging.error( 'scraper(%d), src(%d), id(%s):\n%s',
                                self._scraper_id, src_id, self._get_post_id(link), traceback.format_exc())
                else:
                    break
            if ( scape_count > 0 ):
                logging.info( 'scraper(%d), src(%d): %d posts saved' ,
                            self._scraper_id, src_id, scape_count )

        except Exception, err:
            logging.error( 'scraper(%d), src(%d):\n%s',
                self._scraper_id, src_id, traceback.format_exc())

    def _get_post_id(self, url):
        prog = re.compile('^.+=(\d+)$')
        result = prog.match(url)
        return result.group(1)

    def _add_tags(self, source_id, post_id):
        for tag_id in dbagent.get_source_tags(source_id):
            dbagent.add_post_tag(post_id, tag_id)


    def scrape(self):
        for src in dbagent.get_sources(self._scraper_id):
            self._scrape(src['id'], src['url'])

        #self._scrape(27, 'http://www.backpackers.com.tw/forum/external.php?type=RSS2&amp;forumids=309')
        
        #print(self._sources())
        #for src in self._sources():
        #    self._scrape(src)
        
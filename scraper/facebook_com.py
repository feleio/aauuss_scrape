# -*- coding: utf-8 -*-
import re
import logging
import traceback
import simplejson

from datetime import datetime

#my modules
import dbagent
import url

class Scraper:
    def __init__(self):
        self._scraper_id = 2
        self._token = "CAALN1209ZAmgBAJo0S4ZAGhb4obyPAuft8O4DehKmaELyEbJ5QnAvqpoou9nGlZBvd15wFEhti7z1E9kZCzE4gHE8GQusq4HXUgRaZAWfZBImuWHdLZBzyw6LJwVDEH8eqL0ADZBZBo8gVj99STZAnTWaqxlPZAP8oR2jRdxBxXqZCdzojE6BtZA6k7ST"
        dbagent.set_time_zone('+00:00')

    def _scrape(self, run_id, src_id, src_remote_id):
        try:
            scrape_id = dbagent.get_scrape_id(run_id, src_id)
            logging.debug( 'scraper(%d), src(%d) start:' ,
                            self._scraper_id, src_id, extra={'scrape_id':scrape_id} )
            src_url = ("https://graph.facebook.com/v2.3/%s/feed?access_token=%s" 
                    % (src_remote_id, self._token))

            scape_count = 0
            err_count = 0
            json = simplejson.load(url.get(src_url))

            for post in json['data']:
                remote_id = post['id']
                if(not dbagent.is_post_exist(src_id, remote_id)):
                    try:
                        if('message' in post):
                            splits = post['message'].split('\n',1)
                            title = splits[0]
                            content = splits[1] if (len(splits) > 1) else ''
                        elif('description' in post):
                            splits = post['description'].split('\n',1)
                            title = splits[0]
                            content = splits[1] if (len(splits) > 1) else ''
                        else:
                            title = '(請點連結閱讀內容)'
                            content = ''
                        title = title[:30] if (len(title) > 30) else title
                        
                        link = "https://www.facebook.com/"+post['id']
                        author = post['from']['name']
                        posted_at = datetime.strptime(post['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
                        #print ('scraper(%d), src(%d): id: %s' % (self._scraper_id, src_id, remote_id))
                        new_post_id = dbagent.add_post(title, content, link, author, src_id, remote_id, posted_at)
                        self._add_tags(src_id, new_post_id)
                        scape_count += 1
                    except Exception, err:
                        logging.error( 'scraper(%d), src(%d), id(%s):\n%s',
                                    self._scraper_id, src_id, remote_id, traceback.format_exc(), extra={'scrape_id':scrape_id})
                        dbagent.source_error(src_id)
                        err_count += 1

            if ( scape_count > 0 ):
                logging.info( 'scraper(%d), src(%d): %d posts saved', 
                        self._scraper_id, src_id, scape_count, extra={'scrape_id':scrape_id})
                dbagent.source_scrape(src_id, scape_count)

            if (err_count > 0):
                dbagent.update_scrape_status(run_id, src_id, 'fail')
            else:
                dbagent.update_scrape_status(run_id, src_id, 'success')
                
        except Exception, err:
            logging.error( 'scraper(%d), src(%d):\n%s' ,
                        self._scraper_id, src_id, traceback.format_exc(), extra={'scrape_id':scrape_id})
            dbagent.source_error(src_id)
            dbagent.update_scrape_status(run_id, src_id, 'fail')

    # def _get_post_id(self, url):
    #     prog = re.compile('^.+=(\d+)$')
    #     result = prog.match(url)
    #     return result.group(1)

    def _add_tags(self, source_id, post_id):
        for tag_id in dbagent.get_source_tags(source_id):
            dbagent.add_post_tag(post_id, tag_id)

    def scrape(self, run_id):
        for src in dbagent.get_sources(self._scraper_id):
            self._scrape(run_id, src['id'], src['url'])

        #self._scrape(27, 'http://www.backpackers.com.tw/forum/external.php?type=RSS2&amp;forumids=309')
        
        #print(self._sources())
        #for src in self._sources():
        #    self._scrape(src)
        
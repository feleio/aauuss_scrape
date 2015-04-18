from scraper import *
import time
while 1:
    
    s = backpackers_com_tw.Scraper()
    s.scrape()

    s = facebook_com.Scraper()
    s.scrape()

    time.sleep(5*60) # delays for 5 seconds
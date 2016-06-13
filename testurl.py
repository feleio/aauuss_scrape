#import newurl
import pprint
import urllib2

proxy = urllib2.ProxyHandler({'http':'120.85.132.234:80'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)

print urllib2._opener.handle_open['http']
print vars(urllib2._opener.handle_open['http'][0])

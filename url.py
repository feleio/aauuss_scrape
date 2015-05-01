import urllib2
import socket


def get(url):
    if(socket.gethostname() != "homestead"):
        proxy = urllib2.ProxyHandler({'http':'58.152.34.72:8080'})
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)

    hdr = {'Accept-Encoding': 'deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    return response

import urllib2
import socket

class Url:
    def getHandle_open(self):
        return urllib2._opener.handle_open['http'][0]
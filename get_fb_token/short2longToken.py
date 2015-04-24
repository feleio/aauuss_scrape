import simplejson
import urllib2
import re

short_token = "CAALN1209ZAmgBAPtmOvT3gmvCQdV2XZCqeaNvuRikvCDvwSk2I5Ao2rsi9Ubq9uAd2wtUSbFZBpn0ZB1AApZBBIr4KwCLQ7UZCHobryNSyPZBxf4tQ6ctXJpSHs1sVlTyFAWlI95ZC8Q3W1T57G25wu6bAnJPjxBgV824ENy4FUKc5KkLyZAlX3WHwvAeRlzHSgaBeuzPej0zTfHdYYlDTI4a"
app_id = "789275087824488"
app_secret = "960d332f0b7d030c3e18befbfcc91777"

url = 	"https://graph.facebook.com/oauth/access_token?" \
	    "grant_type=fb_exchange_token&" \
	    "client_id=" + app_id + "&" \
	    "client_secret=" + app_secret + "&" \
	    "fb_exchange_token=" + short_token

f_url = open('url.txt', 'w')
f_url.write(url)


response = urllib2.urlopen(url)
#json = simplejson.load(response.read())

result = response.read().decode('utf-8')
print(result)
m = re.search(r'access_token=(.+)&', result);
token = m.group(1);
print(token)

f_token = open('long_token.txt', 'w')
f_token.write(token)



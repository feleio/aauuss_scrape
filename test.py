from bs4 import BeautifulSoup
import re

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<div class="what the">
<a href="http://example.com/felix" class="sister" id="link1">Felix</a>,
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
</div>
<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, "html.parser")

url = 'http://www.backpackers.com.tw/forum/forumdisplay.php?f=310'
prog = re.compile('^.+f=(\d+)$')
result = prog.match(url,)
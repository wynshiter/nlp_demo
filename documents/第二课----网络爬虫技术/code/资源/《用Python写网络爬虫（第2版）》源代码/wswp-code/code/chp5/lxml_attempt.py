from lxml.html import fromstring
from chp3.downloader import Downloader

D = Downloader()
html = D('http://example.python-scraping.com/search')
tree = fromstring(html)
tree.cssselect('div#results a')

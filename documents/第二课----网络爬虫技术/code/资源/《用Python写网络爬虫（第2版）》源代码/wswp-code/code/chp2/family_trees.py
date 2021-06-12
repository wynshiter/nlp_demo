from lxml.html import fromstring
from chp1.advanced_link_crawler import download

url = 'http://example.python-scraping.com/view/UnitedKingdom-233'
html = download(url)

tree = fromstring(html)
table = tree.xpath('//table')[0]

print('Children:', table.getchildren())
print('Parent:', table.getparent())
print('Previous Sibling:', table.getprevious())
print('Next Sibling:', table.getnext())
print('All Siblings:', list(table.itersiblings()))

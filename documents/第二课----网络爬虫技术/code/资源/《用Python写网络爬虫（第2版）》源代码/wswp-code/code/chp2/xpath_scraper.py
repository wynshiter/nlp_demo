from lxml.html import fromstring
from chp1.advanced_link_crawler import download

url = 'http://example.python-scraping.com/view/UnitedKingdom-233'
html = download(url)

tree = fromstring(html)
area = tree.xpath('//tr[@id="places_area__row"]/td[@class="w2p_fw"]/text()')[0]
print(area)

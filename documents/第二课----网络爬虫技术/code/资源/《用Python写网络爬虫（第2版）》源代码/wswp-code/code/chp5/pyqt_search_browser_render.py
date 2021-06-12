from chp5.browser_render import BrowserRender

br = BrowserRender()
br.download('http://example.python-scraping.com/search')
br.attr('#search_term', 'value', '.')
br.text('#page_size option:checked', '1000')
br.click('#search')
elements = br.wait_load('#results a')

countries_or_districts = [e.toPlainText().strip() for e in elements]
print(countries_or_districts)

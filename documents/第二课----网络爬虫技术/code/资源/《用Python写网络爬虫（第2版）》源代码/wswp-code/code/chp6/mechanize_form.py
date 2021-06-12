import mechanize

LOGIN_URL = 'http://example.python-scraping.com/user/login'
LOGIN_EMAIL = 'example@python-scraping.com'
LOGIN_PASSWORD = 'example'
COUNTRY_OR_DISTRICT_URL = 'http://example.python-scraping.com/edit/United-Kingdom-233'


br = mechanize.Browser()
br.open(LOGIN_URL)
br.select_form(nr=0)
br['email'] = LOGIN_EMAIL
br['password'] = LOGIN_PASSWORD
response = br.submit()
br.open(COUNTRY_OR_DISTRICT_URL)
br.select_form(nr=0)
br['population'] = str(int(br['population']) + 1)
br.submit()

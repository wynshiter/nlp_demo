import requests

LOGIN_URL = 'http://example.python-scraping.com/user/login'
LOGIN_EMAIL = 'example@python-scraping.com'
LOGIN_PASSWORD = 'example'
data = {'email': LOGIN_EMAIL, 'password': LOGIN_PASSWORD}

response = requests.post(LOGIN_URL, data)
print(response.url)

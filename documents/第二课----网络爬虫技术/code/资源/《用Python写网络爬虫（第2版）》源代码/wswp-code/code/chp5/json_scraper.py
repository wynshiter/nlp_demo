import requests
import string

PAGE_SIZE = 10

template_url = 'http://example.python-scraping.com/ajax/' + \
    'search.json?page={}&page_size={}&search_term={}'

countries_or_districts = set()

for letter in string.ascii_lowercase:
    print('Searching with %s' % letter)
    page = 0
    while True:
        resp = requests.get(template_url.format(page, PAGE_SIZE, letter))
        data = resp.json()
        print('adding %d more records from page %d' %
              (len(data.get('records')), page))
        for record in data.get('records'):
            countries_or_districts.add(record['country_or_district'])
        page += 1
        if page >= data['num_pages']:
            break

with open('../data/countries_or_districts.txt', 'w') as countries_or_districts_file:
    countrie_or_districts_file.write('\n'.join(sorted(countries_or_districts)))

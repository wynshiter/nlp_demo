# encoding: utf-8
'''
@author: season
@contact: seasonwang@insightzen.com

@file: test.py.py
@time: 2018/11/1 16:10
@desc:
'''
import re

page_link = 'https://blog.csdn.net/Insightzen_xian/article/details/82263182'

str_page_url_prefix = 'https://blog.csdn.net/Insightzen_xian/'

list_page_str = str_page_url_prefix + 'article/list/'

page_url_pattern = "(" + str_page_url_prefix +")"+ "(article/details)"+"(/[0-9]+)*$"

print(page_url_pattern)

pattern = re.compile(page_url_pattern)
print(pattern)

m = pattern.match(page_link)
print(m)
print(page_link)

if re.match(page_url_pattern, page_link):
    print('ok')
else:
    pass
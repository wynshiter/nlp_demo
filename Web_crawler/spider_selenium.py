# encoding: utf-8
'''
@author: season
@contact: shiter@live.cn

@file: spider_selenium.py
@time: 2019/1/7 22:40
@desc:

使用selenium 进行困难问题的爬取，部分网页内容为动态内容
'''

#

import selenium
from selenium import webdriver
from bs4 import BeautifulSoup


def get_csdn_page_index(url,class_name):
    try:

        browser = webdriver.Chrome()
        browser.get(url)
        browser.implicitly_wait(1)


    #找到共有多少页,如果 selenium 的查找api 找不到，可以用BeautifulSoup 进行查找
        # page_html = browser.page_source
        #
        # bsObj = BeautifulSoup(page_html, "html.parser")
        # page_index = bsObj.findAll(name='li', attrs={'class': 'ui-pager'})

    #text = browser.find_element_by_xpath('//li') # 或者逐层调试查找
    # 很奇怪，用  下面api 找不到这个页码
    #page_number = (browser.find_elements_by_xpath(str_xpath))
        convert_int = lambda x: int(x)  if x.isnumeric()  else -1
        page_number = max([convert_int(i.text) for i in browser.find_elements_by_class_name(class_name)])
    #browser.find_element_by_css_selector('')

        return  page_number

    # except OSError as e:
    #     print(e)
    except Exception as e:
        print(e)
        return 0
# encoding: utf-8
'''
@author: season
@contact: shiter@live.cn

@file: init.py.py
@time: 2019/1/8 15:38
@desc:
'''





import sys
import os
###-----以下导入 其他文件夹的包

CURRENT_URL = os.path.dirname(__file__)
PARENT_URL = os.path.abspath(os.path.join(CURRENT_URL, os.pardir))
sys.path.append(PARENT_URL)

print(PARENT_URL)

# from src import assistance_tool
# ee = assistance_tool.clean_csdn_date('dfdf')
# print(ee)
# import re
# str_page_url_prefix = 'https://blog.csdn.net/wangyaninglm/'
# page_link_pattern = "(" + str_page_url_prefix + ")"
# if re.match(page_link_pattern,'https://blog.csdn.net/wangyaninglm/article/details/51912766'):
#     print(1)
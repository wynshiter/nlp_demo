# encoding: utf-8
'''
@author: season
@contact: shiter@live.cn

@file: __init__.py.py
@time: 2019/1/9 9:56
@desc:
'''

import sys
import os

CURRENT_URL = os.path.dirname(__file__)
PARENT_URL = os.path.abspath(os.path.join(CURRENT_URL, os.pardir))
sys.path.append(PARENT_URL)

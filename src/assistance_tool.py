# encoding: utf-8
'''
@author: season
@contact: shiter@live.cn

@file: assistance_tool.py
@time: 2019/1/8 15:18
@desc:  一些协助工具
'''

import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
#print(parentUrl)
sys.path.append(parentUrl)

import time

def clean_csdn_date(str_date):
    if str_date=='':
        return ''
    else:
        str_date = str_date.replace('年','/').replace('月','/').replace('日','/')
        #timeStruct = time.strptime(str_date, "%Y/%m/%d %H:%M:%S")
        return str_date


def set_starttime():
    start = time.clock()

    return start

#当中是你的程序

def get_runtime(start_time):


    elapsed = (time.clock() - start_time)
    print("Time used:",elapsed)


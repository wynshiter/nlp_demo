#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
'''
@Author  :   {SEASON}
@License :   (C) Copyright 2013-2022, {OLD_IT_WANG}
@Contact :   {shiter@live.cn}
@Software:   PyCharm
@File    :   NLP_DEMO -- regular_expression
@Time    :   2020/5/8 9:33
@Desc    :

'''
#-------------------------------------------------------------------------------


#-*-coding:utf-8-*-

import re

def read_file(filename):
    with open(filename, encoding='utf-8') as fd:
        for line in fd:
            yield line

if __name__== "__main__":

    filename = "templeArticles.txt"
    #匹配以title：为行首开头的字串
    title = re.compile(r'^title:')
    #匹配以位于开头, 中间包含任意字符，的第一句话
    weiyu = re.compile(r'位于((.*?)[。])')
    #匹配以始建于开头，后不直接连接（，或；或。），中间包含任意字符的一句或分句
    shijianyu = re.compile(r'始建于(((?!，|；|。).)+)(，|；|。)')

    for line in read_file(filename):
        # 处理文件每一行文件
        if re.match(title,line):
            print(line[6:-1])

        if re.findall(weiyu,line):
            print('位于: ' + re.findall(weiyu,line)[0][0])

        if re.findall(shijianyu,line):
            print('始建于：' + re.findall(shijianyu,line)[0][0])




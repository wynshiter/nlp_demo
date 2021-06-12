#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
'''
@Author  :   {SEASON}
@License :   (C) Copyright 2013-2022, {OLD_IT_WANG}
@Contact :   {shiter@live.cn}
@Software:   PyCharm
@File    :   NLP_DEMO -- jiagu_segmentation.py
@Time    :   2020/7/30 19:51
@Desc    :

'''
#-------------------------------------------------------------------------------
import jiagu

#jiagu.init() # 可手动初始化，也可以动态初始化

text = '今天天气不错，挺风和日丽的，我们下午没有课'

words = jiagu.seg(text) # 分词
print(words)

pos = jiagu.pos(words) # 词性标注
print(pos)

ner = jiagu.ner(words) # 命名实体识别
print(ner)
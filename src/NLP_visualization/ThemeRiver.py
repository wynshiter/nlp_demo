#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
'''
@Author  :   {SEASON}
@License :   (C) Copyright 2013-2022, {OLD_IT_WANG}
@Contact :   {shiter@live.cn}
@Software:   PyCharm
@File    :   NLP_DEMO -- ThemeRiver
@Time    :   2020/9/13 23:14
@Desc    :

'''
#-------------------------------------------------------------------------------


import re
import jieba
import pandas as pd
import openpyxl
import pyecharts.options as opts
from pyecharts.charts import ThemeRiver


from Database import blog, mySQLiteForblog
from src import assistance_tool

#
# def find(word,words,num):
#     list = []
#     sum_num = len(words)
#     step = int(sum_num / num)
#     for i in range(num):
#         total = 0
#         list_1=[i]
#         new_list = words [i*step:(i+1)*step]
#         for new_word in new_list:
#             if new_word==word :
#                 total+=1
#         list_1.append(total)
#         list_1.append(word)
#         list.append(list_1)
#     return list
#
# txt=open("../../blog/1000.txt",encoding='utf-8',mode='r').read()
#
#
# words=jieba.lcut(txt)
#
# count={}
# sum = len(words)
#
# for word in words:
#     if len(word)==1:
#         continue
#     else:
#         count[word]=count.get(word,0)+1
#
# items=list(count.items())
# items.sort(key=lambda x:x[-1],reverse=True)
#
# # 主题
# x_data=[]
#
# y_data=[]
#
# for word in range(5):
#     x_data.append(items[word][0])
#
# for ci in x_data:
#     y = find(ci, words, 20)
#     for i in y:
#         y_data.append(i)
#
# ThemeRiver(init_opts=opts.InitOpts(width="1600px", height="800px")).add(
#         series_name=x_data,
#         data=y_data,
#         label_opts=opts.LabelOpts(font_size = 18),
#         singleaxis_opts=opts.SingleAxisOpts(
#             pos_top="50", pos_bottom="50"
#         ),
#     ).set_global_opts(
#         tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="line")
#     ).render("theme_river.html")

## 从所有博客主题中提取博客内容涉及最多的几个主题 ，做时间维度的主题河流

STR_PATH_SQLITE = 'sqlite:///../../Database/NLP_demo.db?check_same_thread=False'

DBSession = mySQLiteForblog.get_conn(STR_PATH_SQLITE, True)

table_and_column_name = blog.CsdnBlog
filter = (blog.CsdnBlog.title == 'AutoML与机器学习领域的理解')

all_blog_label = DBSession.query(table_and_column_name.label).all()

print(all_blog_label)

df = pd.DataFrame(DBSession.query(table_and_column_name).all())


print(all_blog_label)
# encoding: utf-8
'''
@author: season
@contact: shiter@live.cn

@file: CSDN_Blog.py
@time: 2019/1/7 10:34
@desc:
'''

import sys
import os
from sqlalchemy import Column, TEXT, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

# from sqlalchemy.orm import scoped_session, sessionmaker

CURRENT_URL = os.path.dirname(__file__)
PARENT_URL = os.path.abspath(os.path.join(CURRENT_URL, os.pardir))
sys.path.append(PARENT_URL)

COLUMN_NAME = ['article_id',
                   'title',
                   'content',
                   'create_time',
                   'click_number',
                   'comment_number',
                   'label',
                   'article_type',
                   'number_of_labels',
                   'create_time_year',
                   'create_time_month',
                   'create_time_week',
                   'create_time_hour'
                   ]


Base = declarative_base()


class CsdnBlog(Base):
    '''
    # 定义blog 文章对象:
    文章id，标题，内容，创建时间，点击数，评论数，标签，文章类型，标签数，创建年份，创建月份，创建文章是星期几，
    待增加的特征：摘要，文章字数，文章图片数
    '''
    __tablename__ = 'CSDN_Blog'

    # 表的结构:

    article_id = Column(String(64), primary_key=True, unique=True)
    title = Column(String(256))
    content = Column(TEXT)
    create_time = Column(DateTime)
    click_number = Column(Integer)
    comment_number = Column(Integer)
    label = Column(TEXT)
    article_type = Column(String(64))
    number_of_labels = Column(Integer)
    create_time_year = Column(Integer)
    create_time_month = Column(Integer)
    create_time_week = Column(Integer)
    create_time_hour = Column(Integer)

    def __repr__(self):
        return "<CSDN_Blog(article_id ='%s' ," \
               " title = '%s', " \
               "contend = '%s', " \
               "create_time = '%s', " \
               "click_number = '%s', " \
               "comment_number = '%s', " \
               "label = '%s', " \
               "article_type = '%s', " \
               "number_of_labels = '%s', " \
               "create_time_year = '%s', " \
               "create_time_month = '%s', " \
               "create_time_week = '%s' ," \
               "create_time_housr = '%s')>" % (
                   self.article_id,
                   self.title,
                   self.content,
                   self.create_time,
                   self.click_number,
                   self.comment_number,
                   self.label,
                   self.article_type,
                   self.number_of_labels,
                   self.create_time_year,
                   self.create_time_month,
                   self.create_time_week,
                   self.create_time_hour
               )
    #试了一下不用初始化函数也可以初始化类，这块的继承关系还不是很理解
    # def __init__(self,
    #              article_id,
    #              title, content,
    #              create_time,
    #              click_number,
    #              comment_number,
    #              label,
    #              article_type,
    #              number_of_labels,
    #              create_time_year,
    #              create_time_month,
    #              create_time_week,
    #              create_time_hour):
    #     self.article_id = article_id
    #     self.title = title
    #     self.content = content
    #     self.create_time = create_time
    #     self.click_number = click_number
    #     self.comment_number = comment_number
    #     self.label = label
    #     self.article_type = article_type
    #     self.number_of_labels = number_of_labels
    #     self.create_time_year = create_time_year
    #     self.create_time_month = create_time_month
    #     self.create_time_week = create_time_week
    #     self.create_time_hour = create_time_hour
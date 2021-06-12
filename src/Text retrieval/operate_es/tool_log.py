#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
'''
@Author  :   {SEASON}
@License :   (C) Copyright 2013-2022, {OLD_IT_WANG}
@Contact :   {shiter@live.cn}
@Software:   PyCharm
@File    :   code_mapping -- mylog
@Time    :   2019/9/2 16:52
@Desc    :
@desc:


'''
#-------------------------------------------------------------------------------
# encoding: utf-8


import sys
import os

import logging
from logging import handlers


# CURRENT_URL = os.path.dirname(__file__)
# PARENT_URL = os.path.abspath(os.path.join(CURRENT_URL, os.pardir))
# sys.path.append(PARENT_URL)



class Logger(object):
    '''
    this is my log class, 同时写文件及控制台

    usage:
    log = myLog.Logger('./log/all.log', level='debug')

    myLog.Logger('./log/error.log', level='error').logger.error('error')
    log.logger.debug('starting !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    '''
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }#日志级别关系映射

    def __init__(self,
                 filename,
                 level='info',
                 when='D',
                 backCount=3,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):

        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)#设置日志格式
        self.logger.setLevel(self.level_relations.get(level))#设置日志级别
        streamhandler = logging.StreamHandler()#往屏幕上输出
        streamhandler.setFormatter(format_str) #设置屏幕上显示的格式
        timefilehandler = handlers.TimedRotatingFileHandler(filename=filename,
                                                            when=when,
                                                            backupCount=backCount,
                                                            encoding='utf-8')
        #往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        timefilehandler.setFormatter(format_str)#设置文件里写入的格式
        self.logger.addHandler(streamhandler) #把对象加到logger里
        self.logger.addHandler(timefilehandler)

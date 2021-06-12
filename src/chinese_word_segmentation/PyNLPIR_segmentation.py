#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
'''
@Author  :   {SEASON}
@License :   (C) Copyright 2013-2022, {OLD_IT_WANG}
@Contact :   {shiter@live.cn}
@Software:   PyCharm
@File    :   NLP_DEMO -- PyNLPIR_segmentation
@Time    :   2019/7/17 0:06
@Desc    :

'''
#-------------------------------------------------------------------------------

# import pynlpir
# pynlpir.open()
#
# s = '欢迎科研人员、技术工程师、企事业单位与个人参与NLPIR平台的建设工作。'
# s2 = '乙肝大三阳冠心病都是慢性病'
#
# print(pynlpir.segment(s))
# print(pynlpir.segment(s2))
#
s3 = 'NLPIR分词系统前身为2000年发布的ICTCLAS词法分析系统，从2009年开始，为了和以前工作进行大的区隔，并推广NLPIR自然语言处理与信息检索共享平台，调整命名为NLPIR分词系统。'
# print(pynlpir.segment(s3))
# print(pynlpir.segment(s3, pos_tagging=False))

# 关闭api 节省内存
# pynlpir.close()

from pynlpir import nlpir
import ctypes
print(type(nlpir.PACKAGE_DIR))
#python与传参到c借口编码需要转一下，所有字符串前面加一个b或者转utf-8就可以了。
nlpir.Init((nlpir.PACKAGE_DIR).encode('utf-8'),nlpir.UTF8_CODE,None)

result_seg_test = nlpir.ParagraphProcess(s3.encode('utf-8'), True)
print(result_seg_test.decode('utf-8'))

# size = ctypes.c_int()
# result = nlpir.ParagraphProcessA(s3.encode('utf-8'), ctypes.byref(size), False)
# result_t_vector = ctypes.cast(result, ctypes.POINTER(nlpir.ResultT))
# words = []
# for i in range(0, size.value):
#     r = result_t_vector[i]
#     word = s3[r.start:r.start+r.length]
#     words.append((word, r.sPOS))
#
# print(words)
# nlpir.Exit()


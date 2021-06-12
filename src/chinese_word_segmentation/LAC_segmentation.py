#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
'''
@Author  :   {SEASON}
@License :   (C) Copyright 2013-2022, {OLD_IT_WANG}
@Contact :   {shiter@live.cn}
@Software:   PyCharm
@File    :   NLP_DEMO -- LAC_segmentation.py
@Time    :   2020/10/25 19:20
@Desc    :

pip install lac -i https://mirror.baidu.com/pypi/simple
'''
#-------------------------------------------------------------------------------


from LAC import LAC

# 装载分词模型
lac = LAC(mode='seg')

# 单个样本输入，输入为Unicode编码的字符串
text = u"LAC是个优秀的分词工具"
seg_result = lac.run(text)

# 批量样本输入, 输入为多个句子组成的list，平均速率会更快
texts = [u"LAC是个优秀的分词工具", u"百度是一家高科技公司"]
seg_result = lac.run(texts)
print(seg_result)

# 词性标注

# 装载LAC模型
lac = LAC(mode='lac')

# 单个样本输入，输入为Unicode编码的字符串
text = u"LAC是个优秀的分词工具"
lac_result = lac.run(text)

# 批量样本输入, 输入为多个句子组成的list，平均速率更快
texts = [u"LAC是个优秀的分词工具", u"百度是一家高科技公司"]
lac_result = lac.run(texts)
print(lac_result)
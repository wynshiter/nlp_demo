# encoding: utf-8
'''
@author: season
@contact: shiter@live.cn

@file: word2vector.py
@time: 2018/12/9 23:34
@desc:
'''


from aip import AipNlp

""" 你的 APPID AK SK """
APP_ID = '11395257'
API_KEY = 'xVbGoPnQGyoffrv0YKBvHSS6'
SECRET_KEY = 'oZXwmwD2CTLc8bh9NKPzZM2LxrHySzOB'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

word1 = "张飞"
dict_zhangfei = {}
word2 = "关羽"
dict_liubei = {}

""" 调用词向量表示 """
dict_zhangfei = client.wordEmbedding(word1)
print(dict_zhangfei)
dict_liubei = client.wordEmbedding(word2)
print(dict_liubei)

vector_zhangfei = dict_zhangfei['vec']
vector_liubei = dict_liubei['vec']

import numpy as np
import math
def Cosine(vec1, vec2):
    npvec1, npvec2 = np.array(vec1), np.array(vec2)
    return npvec1.dot(npvec2)/(math.sqrt((npvec1**2).sum()) * math.sqrt((npvec2**2).sum()))
# Cosine，余弦夹角

print(""" 调用词义相似度: """,client.wordSimEmbedding(word1, word2))
print("余弦相似度：",Cosine(vector_zhangfei, vector_liubei))
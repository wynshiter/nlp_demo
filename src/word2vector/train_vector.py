#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
'''
@Author  :   {SEASON}
@License :   (C) Copyright 2013-2022, {OLD_IT_WANG}
@Contact :   {shiter@live.cn}
@Software:   PyCharm
@File    :   NLP_DEMO -- train_vector
@Time    :   2020/9/18 1:02
@Desc    :
https://zhuanlan.zhihu.com/p/194263854
'''
#-------------------------------------------------------------------------------

# 导入模块并设置日志记录
import gensim, logging
from pprint import pprint
from smart_open import smart_open
import os
import jieba

#jieba.load_userdict(r"dictionary.txt")  #载入自定义词典，提高分词的准确性,因为数据量较大，需要花点时间加载
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

# import nltk
# nltk.download('wordnet')
# porter_stemmer = PorterStemmer()
# wordnet_lemmatizer = WordNetLemmatizer()



stoplist = [i.strip() for i in open('../stopwords/stopwords.txt',encoding='utf-8').readlines()]  #载入停用词列表



class MySentences(object):
  def __init__(self, dirname):
    self.dirname = dirname
  def __iter__(self):
    for fname in os.listdir(self.dirname):
      #print('正在处理文件{}'.format(fname))
      for line in smart_open(os.path.join(self.dirname, fname), 'r',encoding='utf-8'):
        line = line.lower() #对每一行文本中的英文词汇小写化
        #line = wordnet_lemmatizer.lemmatize(porter_stemmer.stem(line))
        #line = line.replace('social listening','social_listening')  #'social_listening'是文本中一个重要的词汇，为了防止因分词问题导致的语义丢失，笔者将其替换成带下划线的单个词汇
        #jieba.add_word('social_listening')  #对特定长词进行控制，防止被分错词，影响后续的分析效果
        #jieba.add_word('社会化聆听')  #对social_listening进行控制，防止被分错词，影响后续的分析效果
        yield [i.strip() for i in jieba.lcut(line) if i not in stoplist and  len(i) > 1]  #在载入文本的同时，对其中的语句进行分词处理，且去掉停用词和长度小于1的语句

sentences = MySentences(r'../../blog/')  # 内存友好的迭代器

# data_cut = [jieba.lcut(i) for i  in sentences] #对语句进行分词
# data_cut = [' '.join(jieba.lcut(i)) for i  in sentences] #用空格隔开词汇，形成字符串，便于后续的处理

# sentences = [[word for word in document.strip().split() if word not in stoplist] for document in data_cut]   #过滤语句中的停用词
# sentences[:3]  #展示预处理后语句列表中的3个样例
print(list(sentences)[:10])   #打印其中的30个文档


#model = gensim.models.Word2Vec(sentences, min_count=3)


# print(model)
# print(list(model.wv.vocab)[:50])




# new_model = gensim.models.Word2Vec(min_count=2)  # 一个“空”的模型，还未进行实质性的训练
# new_model.build_vocab(sentences)                 # 可以是不可重复的，遍历一次语句生成器
# new_model.train(sentences, total_examples=new_model.corpus_count, epochs=new_model.iter)   #可以是不可重复的，遍历一次语句生成器


model = gensim.models.Word2Vec(
                             sentences,
                             size = 50,
                             sg=1,
                             min_count= 3,
                             window = 8,
                             iter = 3 )

# from tempfile import mkstemp
# temp_path = mkstemp("gensim_temp.txt")  # 创建一个temp文件
with open('gensim_temp.txt','wb') as f:
    model.save(f)  # 保存模型

#new_model = gensim.models.Word2Vec.load(temp_path)
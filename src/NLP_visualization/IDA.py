# encoding: utf-8
'''
@author: season
@contact: shiter@live.cn

@file: IDA.py
@time: 2018/12/9 23:33
@desc:
'''

import file_operator

import  jieba
import pandas as pd
file_path = r'..\..\blog'
file_list = file_operator.all_Absolute_pathfile_name(file_path,'.txt')


data = pd.DataFrame(file_list,columns=['file_name'])

#分词，暂时没有去停用词
def chinese_word_cut_by_jieba(file_name):
    mytext = ''
    with open(file_name,'r',encoding='utf-8') as f:
        mytext = f.read()
    return " ".join(jieba.cut(mytext))



#新增分词后的字段内容
data["content_cutted"] =data['file_name'].apply(chinese_word_cut_by_jieba)

data_head = data.content_cutted.head()

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
#从文本中提取1000个最重要的特征关键词
n_features = 1000
tf_vectorizer = CountVectorizer(strip_accents = 'unicode',
                                max_features=n_features,
                                stop_words='english',
                                max_df = 0.5,
                                min_df = 10)
tf = tf_vectorizer.fit_transform(data.content_cutted)

from sklearn.decomposition import LatentDirichletAllocation

n_topics = 10

lda = LatentDirichletAllocation(n_components=n_topics, max_iter=50,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)

# lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=50,
#                                 learning_method='online',
#                                 learning_offset=50.,
#                                 random_state=0)


lda.fit(tf)
#显示主题数 model.topic_word_
print(lda.components_)
#几个主题就是几行 多少个关键词就是几列
print(lda.components_.shape)

#计算困惑度
print(u'困惑度：')
print(lda.perplexity(tf,sub_sampling = False))
#
def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()


n_top_words = 20

tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, n_top_words)

import pyLDAvis
import pyLDAvis.sklearn
#pyLDAvis.enable_notebook()
#pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)


data = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
pyLDAvis.show(data)
pyLDAvis.display()
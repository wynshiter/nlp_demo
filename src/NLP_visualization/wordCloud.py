# encoding: utf-8
'''
@author: season
@contact: shiter@live.cn

@file: wordCloud.py
@time: 2018/11/6 22:38
@desc:
'''



import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
import jieba.analyse
import file_operator
# 直接使用plt.imshow无法显示图片，需要导入pylab包
# pycharm 对anaconda中的 matplotlib 支持有问题
#import pylab

file_path = r'../blog'

file_list = file_operator.all_Absolute_pathfile_name(file_path,'.txt')



str_summary = ''

def get_all_strFromTxt(file_name):
    str_blog = ''
    with open(file_name,'r',encoding='utf-8') as f:
        str_blog = f.read()
    return str_blog

for i in file_list:
    str_summary = str_summary + get_all_strFromTxt(i)




def getTopkeyWordsTFIDF(stop_word_file_path,topK=100,content = '',top_word_dict_TFIDF={}):
    try:
        jieba.analyse.set_stop_words(stop_word_file_path)
        tags = jieba.analyse.extract_tags(content, topK, withWeight=True,allowPOS=('ns', 'n', 'vn', 'v'))
        for v, n in tags:
            print (v + '\t' + str((n )))
            top_word_dict_TFIDF[v] = n * 100
            #tfidf *100 作为词频
        return top_word_dict_TFIDF
    except Exception as e:
        print(e)
        return {}
    finally:
        pass


def getTopkeyWordsTextRank(stop_word_file_path, topK=100, content='',top_word_dict_TEXTRANK={}):
    try:
        jieba.analyse.set_stop_words(stop_word_file_path)

        tags = jieba.analyse.textrank(content, topK, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
        for v, n in tags:
            print(v + '\t' + str(((n))))
            top_word_dict_TEXTRANK[v] = n * 100
            # tfidf *100 作为词频
        return top_word_dict_TEXTRANK
    except Exception as e:
        print(e)
        return {}
    finally:
        pass


top_word_dict_TFIDF = {}
top_word_dict_TEXTRANK = {}

getTopkeyWordsTFIDF(r'../documents/stop_words.txt',150,str_summary,top_word_dict_TFIDF)
getTopkeyWordsTextRank(r'../documents/stop_words.txt',150,str_summary,top_word_dict_TEXTRANK)

print(top_word_dict_TFIDF)
print(top_word_dict_TEXTRANK)





stop_words = [' ','版权','声明','博主','原创','转载','本文','未经']



# 可以指定字体，或者按照词频生成
def show_WordCloud(stop_words,top_word,img_name,str_font_path):
    # wordlist_after_jieba = jieba.cut(str_all, cut_all=True)
    # wl_space_split = " ".join(wordlist_after_jieba)
    my_wordcloud = WordCloud(background_color = "white",width = 1000,height = 860,font_path = str_font_path,
                # 设置中文字体
                margin = 2,
    max_words=150, # 设置最大现实的字数
    stopwords=stop_words,# 设置停用词
    max_font_size=250,# 设置字体最大值
    random_state=50# 设置有多少种随机生成状态，即有多少种配色方案

    )
    #my_wordcloud = my_wordcloud.generate(wl_space_split)
    my_wordcloud = my_wordcloud.generate_from_frequencies(top_word)

    plt.imsave(img_name,my_wordcloud)

str_font_path = "../Resources/msyh.ttc"
show_WordCloud(stop_words,top_word_dict_TFIDF,'../image/word_cloud.jpg',str_font_path)



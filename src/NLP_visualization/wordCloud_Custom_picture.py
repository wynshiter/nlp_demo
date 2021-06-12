# encoding: utf-8
'''
@author: season
@contact: shiter@live.cn

@file: wordCloud_Custom_picture.py
@time: 2018/12/17 9:54
@desc:
'''

import os
from os import path
import numpy as np
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
from PIL import Image
from matplotlib import pyplot as plt
from scipy.misc import imread
import random

import chardet
import jieba


import  file_operator

from chinese_word_segmentation import  ltp_segmentation

file_path = r'../blog'

file_list = file_operator.all_Absolute_pathfile_name(file_path,'.txt')

# 所有分词结果，用空格相连
str_summary = ''

def get_all_strFromTxt(file_name):
    str_blog = ''
    with open(file_name,'r',encoding='utf-8') as f:
        str_blog = f.read()
    return str_blog


#空格链接所有分词结果,只要中文
for i in file_list:
    word_seg_list  = ltp_segmentation.segmentor(get_all_strFromTxt(i))
    for j in word_seg_list:
        word = file_operator.is_chinese_word(j)
        if word!=False:
            str_summary = str_summary + word+ ' '


# 设置中文字体
str_font_path = "../Resources/msyh.ttc"
# 读取背景图片
background_Image = np.array(Image.open("../image/csdn.jpg"))
# 提取背景图片颜色
img_colors = ImageColorGenerator(background_Image)
# 设置中文停止词
stopwords = set('')
stopwords.update(['但是','一个','自己','因此','没有','很多','可以','这个','虽然','因为','这样','已经','现在','一些','比如','不是','当然','可能','如果','就是','同时','比如','这些','必须','由于','而且','并且','他们'])

wc = WordCloud(
        font_path = str_font_path, # 中文需设置路径
        margin = 2, # 页面边缘
        mask = background_Image,
        scale = 2,
        max_words = 200, # 最多词个数
        min_font_size = 4, #
        stopwords = stopwords,
        random_state = 42,
        background_color = 'white', # 背景颜色
        # background_color = '#C3481A', # 背景颜色
        max_font_size = 100,
        )




wc.generate(str_summary)
# 获取文本词排序，可调整 stopwords
process_word = WordCloud.process_text(wc,str_summary)
sort = sorted(process_word.items(),key=lambda e:e[1],reverse=True)
print(sort[:50]) # 获取文本词频最高的前50个词
# 设置为背景色，若不想要背景图片颜色，就注释掉
wc.recolor(color_func=img_colors)
# 存储图像
wc.to_file('../image/basic.png')
# 显示图像
plt.imshow(wc,interpolation='bilinear')
plt.axis('off')
plt.tight_layout()
plt.show()
# encoding: utf-8
'''
@author: season
@contact: seasonwang@insightzen.com

@file: file_operator.py
@time: 2018/11/23 15:24
@desc:
'''

import os
import re

def all_pure_file_name_without_extension(file_dir,extension):
    L=[]
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            #print(os.path.splitext(file)[1])
            if os.path.splitext(file)[1] == extension:

                L.append(os.path.splitext(file)[0])
    return L


def all_file_name_with_extension(file_dir,extension):
    L=[]
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            #print(os.path.splitext(file)[1])
            if os.path.splitext(file)[1] == extension:

                L.append(os.path.splitext(file)[0]+os.path.splitext(file)[1])
    return L


def all_Absolute_pathfile_name(file_dir,extension):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == extension:
                L.append(os.path.join(root, file))
    return L


#匹配中文及中文标点符号

#如果全是汉字，返回汉字字符串，如果不是返回false

def is_chinese_word(string_s):
    if len(string_s)<=0:
        return False
    else:

        regex_str = ".*?([\u4E00-\u9FA5])"
        # match_obj = re.match(regex_str, string_s)

        pat = re.compile(regex_str)
        result = pat.findall(string_s)

        if len(result)<=0:
            return False
        else:

            return ''.join(result)


# print(is_chinese_word('wo le我了个去。。拉拉。'))

# pattern = re.compile(u'''[\u4e00-\u9fa5！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏.]+''')
# filterdata = re.findall(pattern, string_s)
# cleaned_comments = ''.join(filterdata)

# #获取当前集合在大集合中没有出现的
# def sub_list(big,small):
#     result = list(set(big).intersection(set(small)))
#     result = list(set(small)-set(result))
#
#     return  result



# l = file_name(r'./html/')
# print(l)
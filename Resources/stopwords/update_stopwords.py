#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
'''
@Author  :   {SEASON}
@License :   (C) Copyright 2013-2022, {OLD_IT_WANG}
@Contact :   {shiter@live.cn}
@Software:   PyCharm
@File    :   NLP_DEMO -- update_stopwords
@Time    :   2021/1/3 22:39
@Desc    :

合并本地文件夹中所有 后缀为 stopwords.txt 的文件中的 stopwords 文件
生成结果放在 all_stopwords.txt 中

'''
#-------------------------------------------------------------------------------


import os


def file_name(file_dir,str_suffix):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == str_suffix:
                L.append(os.path.join(root, file))
    return L

def write_stopwords(stopwords_set,file_name):
    with open(file_name,"w",encoding='utf8') as file:
        for i in stopwords_set:
            file.write(i+'\n')
    file.close()


def main():
    # 绝对路径
    file_path = r'''D:/code/python/csdn_nlp/NLP_DEMO/Resources/stopwords/'''

    filename_set = file_name(file_path,'.txt')

    all_stopwords_set = set([])

    for i in filename_set:
        with open(i,'r',encoding='utf-8') as file:
            list_stopwords = file.readlines()
            file.close()
            set_stopwords = set([j.strip('\n') for j in list_stopwords ])
            all_stopwords_set = all_stopwords_set | set_stopwords
            print(len(all_stopwords_set))


    write_stopwords(all_stopwords_set,file_path+'all_stopwords.txt')

    pass


if __name__ == '__main__':
    main()

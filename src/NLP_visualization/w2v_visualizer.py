#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
'''
@Author  :   {SEASON}
@License :   (C) Copyright 2013-2022, {OLD_IT_WANG}
@Contact :   {shiter@live.cn}
@Software:   PyCharm
@File    :   NLP_DEMO -- w2v_visualizer.py
@Time    :   2020/9/21 23:25
@Desc    :

'''
#-------------------------------------------------------------------------------
from gensim.models import KeyedVectors

# Load gensim word2vec
w2v_path = 'D:\code\python\csdn_nlp\word2vector\sgns.target.word-word.dynwin5.thr10.neg5.dim300.iter5\sgns.target.word-word.dynwin5.thr10.neg5.dim300.iter5'
# w2v = KeyedVectors.load_word2vec_format(w2v_path)



import io

# Vector file, `\t` seperated the vectors and `\n` seperate the words
"""
0.1\t0.2\t0.5\t0.9
0.2\t0.1\t5.0\t0.2
0.4\t0.1\t7.0\t0.8
"""
out_v = io.open(r'.\logs\vecs.tsv', 'w', encoding='utf-8')

# Meta data file, `\n` seperated word
"""
token1
token2
token3
"""
out_m = io.open(r'.\logs\meta.tsv', 'w', encoding='utf-8')


word_num = 2000

from tqdm import tqdm # progression bars
import numpy as np

with open(w2v_path,'r+',encoding='utf-8',) as f:
    header = f.readline()
    vocab_size, vector_size = map(int, header.split())
    words, embeddings = [], []
    for line in tqdm(range(word_num)):
        word_list = f.readline().split(' ')
        word = word_list[0]
        vector = word_list[1:-1]

        out_m.write(word + "\n")
        out_v.write('\t'.join([str(x) for x in vector]) + "\n")

        # words.append(word)
        # embeddings.append(np.array(vector))



# Write meta file and vector file
# for index in range(word_num):
#     word = w2v.index2word[index]
#     vec = w2v.vectors[index]
#     out_m.write(word + "\n")
#     out_v.write('\t'.join([str(x) for x in vec]) + "\n")
out_v.close()
out_m.close()

# Then we can visuale using the `http://projector.tensorflow.org/` to visualize those two files.

# 1. Open the Embedding Projector.
# 2. Click on "Load data".
# 3. Upload the two files we created above: vecs.tsv and meta.tsv.
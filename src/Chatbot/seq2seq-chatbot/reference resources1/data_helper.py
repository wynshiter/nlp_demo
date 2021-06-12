#coding=utf-8
import pickle
import re
import jieba
import pickle
from tqdm import tqdm
from random import randint
import numpy as np
from params import Params as pm
import codecs
import os
from collections import Counter
import torch

FILE_PATH = r"./data/xiaohuangji50w_nofenci.conv"
PKL_FILE = r"./data/xiaohuangji.pkl"

def read_convs():

    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        conversations = []
        # 明确该数据集不是多轮对话
        lines = f.readlines()
        conv = []
        for line in lines:
            if line.startswith('E'):
                # 存储上一轮对话，并置空
                if len(conv) > 0:
                    conversations.append(conv)
                    conv = []
                else:
                    continue
            else:
                line = line.replace('\n','')
                if line.startswith('M'):
                    line = line[1:].strip()#去掉M标记
                    # print(line)
                    conv.append(line)
        conversations.append(conv)
        return conversations

def saveQA(OUTPUT_FILE, questions, answers):
    # 转储成pkl文件，直接保存list方便
    f = open(OUTPUT_FILE,'wb')
    pickle.dump((questions, answers), f)
    f.close()
    print("dump finish")

# 读取对话把对话数组分拆成问答对
def read_conversation(conversations):

    # 读取对话
    questions = []
    answers = []
    print("对话个数:", len(conversations))
    for conv in conversations:
        conv_len = len(conv)
        #print(conv)
        #exit()
        # 对话并不是只有两句,处理成一问一答形式
        if conv_len % 2 != 0:
            conv_len = len(conv) - 1
            questions.append(conv[-2])#倒数第二句为问题
            answers.append(conv[-1])#倒数第一句为答案  
        for i in range(conv_len):
            if i % 2 == 0:
                questions.append(conv[0])
            else:
                answers.append(conv[1])   
    #存储Q和A
    saveQA(PKL_FILE,questions, answers)
    return questions, answers

def regular(sen):
    """整理句子"""
    sen = re.sub(r'\.{3,100}', '…', sen)
    sen = re.sub(r'…{2,100}', '…', sen)
    sen = re.sub(r'[,]{1,100}', '，', sen)
    sen = re.sub(r'[\.]{1,100}', '。', sen)
    sen = re.sub(r'[\?]{1,100}', '？', sen)
    sen = re.sub(r'[*]{1,100}', '！', sen)
    sen = re.sub(r'[@]{2,}', '！', sen)
    sen = re.sub(r'[#]{2,}', '！', sen)
    sen = re.sub(r'[￥|$]{1,}', '！', sen)
    sen = re.sub(r'[|\^]{2,}', '！', sen)
    sen = re.sub(r'[|\&]{2,}', '！', sen)
    sen = re.sub(r'[|\*]{2,}', '！', sen)
    sen = re.sub(r'[!]{2,100}', '！', sen)
    sen = re.sub(r'[！]{2,100}', '！', sen)
    return sen

# 分词
def kepchinese():
    target_fileQ = r"./data/test/cutQ.txt"
    target_fileA = r"./data/test/cutA.txt"
    f = open("./data/xiaohuangji.pkl",'rb')
    questions, answers = pickle.load(f)

    assert len(questions) == len(answers)
    q_list = []
    a_list = []
    for idx in range(len(questions)):
        Q = questions[idx]
        A = answers[idx]
        #print("```",Q)
        Q = format_str(Q)
        #print("---",Q)
        A = format_str(A)
        # 只要有一个为空，就把对话去掉
        if not Q.strip() or not A.strip():
            continue
        q_list.append(Q)
        a_list.append(A)

    # 分词
    assert len(q_list) == len(a_list)
    new_qlist = []
    new_alist = []
    for q, a in tqdm(zip(q_list, a_list)):
        q = jieba.cut(q)
        a = jieba.cut(a)
        new_qlist.append(q)
        new_alist.append(a)
    writefile(new_qlist, target_fileQ)
    writefile(new_alist, target_fileA)
    print("generate test file completed!")
    f.close()


# 让文本只保留汉字
def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

def format_str(content):
    content_str = ''
    for i in content:
        if is_chinese(i):
            content_str = content_str + i
    return content_str

def writefile(doc, filepath):
    '''
    把分好词的文本写入到文件中
    Args:
        doc：文本list
    '''
    #分隔符
    sep = ' ' 
    with open(filepath, 'w+', encoding='utf-8') as f:
        for sequence in doc:
            newsequence=sep.join(sequence)
            f.write(newsequence +"\n")
        print("write finished!")

'''
切分训练集和测试集
'''
VAL_NUM = 1000 #验证集个数
SRC_FILE = r"./data/test/cutQ.txt"
TAG_FILE = r"./data/test/cutA.txt"
TRA_SRC_FILE = r"./data/test/cutQ_train.txt"
TRA_TAG_FILE = r"./data/test/cutA_train.txt"
VAL_SRC_FILE = r"./data/test/cutQ_valid.txt"
VAL_TAG_FILE = r"./data/test/cutA_valid.txt"

#切分训练集和测试集 
def split_data():
    src_val_set, tag_val_set = read_and_split()    
    write_val(src_val_set, tag_val_set)

def read_and_split():
    
    with open(SRC_FILE, 'r', encoding="utf-8") as sf,  \
            open(TAG_FILE, 'r', encoding='utf-8') as tf, \
            open(TRA_SRC_FILE, 'w', encoding='utf-8') as ts, \
            open(TRA_TAG_FILE, 'w', encoding='utf-8') as tt:
        src_lines = sf.readlines()
        tag_lines = tf.readlines()
        assert len(src_lines) == len(tag_lines)
        totalnum = len(src_lines)
        src_val_set = []
        tag_val_set = []
        count = 0
        while count < VAL_NUM:
            randidx =  randint(1, totalnum) 
            if randidx < VAL_NUM:
                count += 1
                src_val_set.append(src_lines.pop(randidx))
                tag_val_set.append(tag_lines.pop(randidx))
        ts.writelines(src_lines)
        tt.writelines(tag_lines)
    return src_val_set, tag_val_set

def write_val(src_val_set, tag_val_set):
    
    with open(VAL_SRC_FILE, 'w', encoding='utf-8') as sf,\
            open(VAL_TAG_FILE, 'w', encoding='utf-8') as tf:
        
        for val in src_val_set:
            val = val.strip()
            sf.write(val + '\n')
        
        for val in tag_val_set:
            val = val.strip()
            tf.write(val + '\n')

def make_train_dic():
    make_dic(pm.src_train, "test_en.vocab.tsv")
    make_dic(pm.tgt_train, "test_de.vocab.tsv")
    print("MSG : Constructing Dictionary Finished!")

def make_dic(path, fname):

    text = codecs.open(path, 'r', 'utf-8').read()
    words = text.split()
    wordCount = Counter(words)
    if not os.path.exists('dictionary'):
        os.mkdir('dictionary')
    with codecs.open('dictionary/{}'.format(fname), 'w', 'utf-8') as f:
        # "<PAD>"= 0,不足长度的文本在后边填充0 "<UNK>" = 1,表示句子中出现的字典中没有的未知词 "<STR>" = 2,表示句子的开头 "<EOS>" = 3,表示句子的结尾
        f.write("{}\t1000000000\n{}\t1000000000\n{}\t1000000000\n{}\t1000000000\n".format("<PAD>","<UNK>","<STR>","<EOS>"))
        
        for word, count in wordCount.most_common(len(wordCount)):
            f.write(u"{}\t{}\n".format(word, count))

def load_vocab(vocab):
    vocab = [line.split()[0] for line in codecs.open('./dictionary/{}'.format(vocab), 'r', 'utf-8').read().splitlines() if int(line.split()[1]) >= pm.word_limit_size]
    word2idx_dic = {word: idx for idx, word in enumerate(vocab)}
    idx2word_dic = {idx: word for idx, word in enumerate(vocab)}
    return word2idx_dic, idx2word_dic

def getword_idx():
    # 获得词索引的方法
    en2idx, idx2en = load_vocab(pm.enc_vocab)
    de2idx, idx2de = load_vocab(pm.dec_vocab)
    return en2idx, idx2en, de2idx, idx2de

# 句子转换成id'<PAD>': 0, '<UNK>': 1, '<STR>': 2, '<EOS>': 3
def indexes_from_text(text, char2index):
    return [2] + [char2index.get(c,1) for c in text] + [3]  # 手动添加开始结束标志

def pad_seq(seq, max_length):
    seq += [0 for _ in range(max_length - len(seq))]
    return seq

if __name__ == "__main__":
    #读取原始数据，抽取QA
    conversations = read_convs()
    #分割Q和A
    questions, answers = read_conversation(conversations)
    #清洗Q和A并分词
    kepchinese()
    #切分训练集和测试集
    split_data()
    #从训练集中获取词典
    make_train_dic()

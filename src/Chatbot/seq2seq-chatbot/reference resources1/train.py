#coding=utf-8
import json
import jieba
from matplotlib import ticker
from collections import Counter
import matplotlib.pyplot as plt
import torch
import numpy as np
import codecs
from model import Encoder
from model import Decoder
from model import Seq2Seq
import torch.optim as optim
from torch import nn
from params import Params as pm
from data_helper import indexes_from_text,pad_seq, getword_idx

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)


def build_vocab(texts, n=None):
    #counter = Counter(''.join(texts))  # char level
    words = texts.split()#按词统计
    counter = Counter(words)

    char2index = {w: i for i, (w, c) in enumerate(counter.most_common(n), start=4)}
    char2index['~'] = 0  # pad  不足长度的文本在后边填充0
    char2index['^'] = 1  # sos  表示句子的开头
    char2index['$'] = 2  # eos  表示句子的结尾
    char2index['#'] = 3  # unk  表示句子中出现的字典中没有的未知词

    index2char = {i: w for w, i in char2index.items()}
    return char2index, index2char

#测试小数据
src_strs = codecs.open(pm.src_test, 'r', 'utf-8').read()
trg_strs = codecs.open(pm.src_test, 'r', 'utf-8').read()
#训练
#src_strs = codecs.open(pm.src_train, 'r', 'utf-8').read()
#trg_strs = codecs.open(pm.tgt_train, 'r', 'utf-8').read()

# 获得索引字典
src_c2ix, src_ix2c, trg_c2ix, trg_ix2c = getword_idx()

src_texts = src_strs.split("\r\n")
trg_texts = trg_strs.split("\r\n")

srcs = [str(line).split() for line in src_texts]
trgs = [str(line).split() for line in trg_texts]

# 求最长序列,词片段的个数
max_src_len = max(list(map(len, srcs))) + 2
max_trg_len = max(list(map(len, trgs))) + 2
max_trg_len = pm.max_trg_len # 可手动设置句子长度
print(max_src_len, max_trg_len)


def random_batch(batch_size, src_texts,trg_texts, src_c2ix, trg_c2ix):
    input_seqs, target_seqs = [], []
    # 随机选出样本作为batch
    for i in np.random.choice(len(src_texts), batch_size):
        #print(src_texts[i])
        #print(indexes_from_text(src_texts[i], src_c2ix))
        input_seqs.append(indexes_from_text(src_texts[i], src_c2ix))
        target_seqs.append(indexes_from_text(trg_texts[i], trg_c2ix))

    seq_pairs = sorted(zip(input_seqs, target_seqs), key=lambda p: len(p[0]), reverse=True)#根据序列长度排序
    input_seqs, target_seqs = zip(*seq_pairs)
    #print(input_seqs)
    input_lengths = [len(s) for s in input_seqs]
    #print(input_lengths)
    input_padded = [pad_seq(s, max(input_lengths)) for s in input_seqs]#pad的长度以batch中最长的为准
    #print(input_padded)

    target_lengths = [len(s) for s in target_seqs]
    target_padded = [pad_seq(s, max(target_lengths)) for s in target_seqs]
    
    input_var = torch.LongTensor(input_padded).transpose(0, 1)#转置
    target_var = torch.LongTensor(target_padded).transpose(0, 1)
    input_var = input_var.to(device)
    target_var = target_var.to(device)
    # seq_len x batch_size
    #print(input_var.shape)
    return input_var, input_lengths, target_var, target_lengths

random_batch(3, srcs,trgs, src_c2ix, trg_c2ix)#test
def show_attention(input_words, output_words, attentions):
    # Set up figure with colorbar
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(attentions, cmap='bone')
    fig.colorbar(cax)

    # Set up axes
    ax.set_xticklabels([''] + input_words)
    ax.set_yticklabels([''] + output_words)

    # Show label at every tick
    ax.xaxis.set_major_locator(ticker.MultipleLocator())
    ax.yaxis.set_major_locator(ticker.MultipleLocator())

    plt.show()
    plt.close()

def evaluate(seq2seqModel, text, src_c2ix, trg_ix2c):
    seq2seqModel.eval()
    with torch.no_grad():
        seq = torch.LongTensor(indexes_from_text(text, src_c2ix)).view(-1, 1).to(device)
        print(seq)
        print([seq.size(0)])
        print(max_trg_len)
        outputs, attn_weights = seq2seqModel.predict(seq, [seq.size(0)], max_trg_len)
        outputs = outputs.squeeze(1).cpu().numpy()
        attn_weights = attn_weights.squeeze(1).cpu().numpy()
        output_words = [trg_ix2c[np.argmax(word_prob)] for word_prob in outputs]
        print(output_words)

        #show_attention(list('^' + text + '$'), output_words, attn_weights)


encoder = Encoder(len(src_c2ix) + 1, pm.embedding_dim, pm.hidden_dim,dropout=pm.dropout)
decoder = Decoder(len(trg_c2ix) + 1, pm.embedding_dim, pm.hidden_dim,dropout=pm.dropout)

seq2seqModel = Seq2Seq(encoder, decoder, device).to(device)

optimizer = optim.Adam(seq2seqModel.parameters())

criterion = nn.NLLLoss(ignore_index=0).to(device)

for epoch in range(pm.num_epochs):

	batch_id = len(srcs)
	for batch_id in range(1, int(batch_id/pm.batch_size)):

	    seq2seqModel.train()
	    src_seqs, src_lengths, trg_seqs, _ = random_batch(pm.batch_size, srcs, trgs, src_c2ix, trg_c2ix)

	    optimizer.zero_grad()
	    output = seq2seqModel(src_seqs, src_lengths, trg_seqs)

	    loss = criterion(output.contiguous().view(-1, output.shape[2]), trg_seqs.contiguous().view(-1))
	    loss.backward()
	    torch.nn.utils.clip_grad_norm_(seq2seqModel.parameters(), pm.clip)
	    optimizer.step()

	    if batch_id % 50 == 0:
	        print('current loss: {:.4f}'.format(loss))
	        text = '我是小黄鸡'

	        evaluate(seq2seqModel, list(jieba.cut(text)), src_c2ix, trg_ix2c)
	#每轮保存一次模型        
	torch.save(seq2seqModel, pm.checkpoint+'/model.pt')
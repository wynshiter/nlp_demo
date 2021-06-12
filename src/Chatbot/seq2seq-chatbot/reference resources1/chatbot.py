# -*- coding: utf-8 -*-
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
import jieba

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)
# 获得索引字典
src_c2ix, src_ix2c, trg_c2ix, trg_ix2c = getword_idx()

# 读取模型
s2s_model = torch.load(pm.checkpoint+'/model.pt')
#print(s2s_model)

def chatbot():

	s2s_model.eval()
	with torch.no_grad():
		while True:
			X = input("you>")
			X = list(jieba.cut(X))
			seq = torch.LongTensor(indexes_from_text(X, src_c2ix)).view(-1, 1).to(device)
			#print(seq)
			outputs, attn_weights = s2s_model.predict(seq, [seq.size(0)], pm.max_trg_len)
			outputs = outputs.squeeze(1).cpu().numpy()
			attn_weights = attn_weights.squeeze(1).cpu().numpy()
			output_words = [trg_ix2c[np.argmax(word_prob)] for word_prob in outputs]
			new_out = []
			for out in output_words:
				out = str(out).strip()
				if out == "<PAD>" or out == "<EOS>" or out == "<STR>":
					continue
				else:
					new_out.append(out)
			new_a = "".join(new_out)
			print(">>",new_a)

if __name__ == "__main__":
	chatbot()
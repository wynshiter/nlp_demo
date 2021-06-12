
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


# 获得索引字典
src_c2ix, src_ix2c, trg_c2ix, trg_ix2c = getword_idx()

def evaluate(model, text, src_c2ix, trg_ix2c,device):
    model.eval()
    with torch.no_grad():

        seq = torch.LongTensor(indexes_from_text(text, src_c2ix)).view(-1, 1).to(device)
        print(seq)

        outputs, attn_weights = model.predict(seq, [seq.size(0)], max_trg_len)
        outputs = outputs.squeeze(1).cpu().numpy()
        attn_weights = attn_weights.squeeze(1).cpu().numpy()
        output_words = [trg_ix2c[np.argmax(word_prob)] for word_prob in outputs]

        return output_words


# 读取模型
s2s_model = torch.load(pm.checkpoint+'/model.pt')
print(s2s_model)

max_trg_len = 30
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)

text = '那 是 什么'
output_words = evaluate(s2s_model, str(text).split(), src_c2ix, trg_ix2c，device,max_trg_len)
print(output_words)
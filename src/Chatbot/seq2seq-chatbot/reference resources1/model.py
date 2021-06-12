import numpy as np
import random
import torch
from torch import nn
import torch.nn.functional as F
#Encoder层                                                                                                        
class Encoder(nn.Module):
    def __init__(self, input_dim, embedding_dim, hidden_dim, num_layers=2, dropout=0.2):
        super().__init__()
        self.input_dim = input_dim
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.dropout = dropout
      
        self.embedding = nn.Embedding(input_dim, embedding_dim)
        # 初始化GRU
        self.rnn = nn.GRU(embedding_dim, hidden_dim,
                          num_layers=num_layers, dropout=dropout)
        self.dropout = nn.Dropout(dropout)

    def forward(self, input_seqs, input_lengths, hidden=None):
        # 将句子序列索引，转换成embedding
        embedded = self.dropout(self.embedding(input_seqs))
        # 按列压紧
        packed = torch.nn.utils.rnn.pack_padded_sequence(embedded, input_lengths)
        outputs, hidden = self.rnn(packed, hidden)
        # 填充回原始行列，压紧的pack_padded_sequence的逆向操作
        outputs, output_lengths = torch.nn.utils.rnn.pad_packed_sequence(outputs)
        return outputs, hidden
#Attention层
class Attention(nn.Module):
    def __init__(self, hidden_dim):
        super(Attention, self).__init__()
        self.hidden_dim = hidden_dim
        self.attn = nn.Linear(self.hidden_dim * 2, hidden_dim)
        self.v = nn.Parameter(torch.rand(hidden_dim))
        self.v.data.normal_(mean=0, std=1. / np.sqrt(self.v.size(0)))
 
    def forward(self, hidden, encoder_outputs):
        #  encoder_outputs:(seq_len, batch_size, hidden_size)
        #  hidden:(num_layers * num_directions, batch_size, hidden_size)
        max_len = encoder_outputs.size(0)
        h = hidden[-1].repeat(max_len, 1, 1)
        # (seq_len, batch_size, hidden_size)
        attn_energies = self.score(h, encoder_outputs)  # compute attention score
        return F.softmax(attn_energies, dim=1)  # normalize with softmax
 
    def score(self, hidden, encoder_outputs):
        # (seq_len, batch_size, 2*hidden_size)-> (seq_len, batch_size, hidden_size)
        energy = torch.tanh(self.attn(torch.cat([hidden, encoder_outputs], 2)))
        energy = energy.permute(1, 2, 0)  # (batch_size, hidden_size, seq_len)
        v = self.v.repeat(encoder_outputs.size(1), 1).unsqueeze(1)  # (batch_size, 1, hidden_size)
        energy = torch.bmm(v, energy)  # (batch_size, 1, seq_len)
        return energy.squeeze(1)  # (batch_size, seq_len)
#Attention层      
class Attention2(nn.Module):
    def __init__(self, hidden_dim):
        super(Attention, self).__init__()
        self.hidden_dim = hidden_dim
        # 选择线性函数，实现注意力计算
        self.attn = nn.Linear(self.hidden_dim , hidden_dim)

    def forward(self, hidden, encoder_outputs):
        max_len = encoder_outputs.size(0)
        h = hidden[-1].repeat(max_len, 1, 1)
        attn_energies = self.score(h, encoder_outputs)  
        return F.softmax(attn_energies, dim=1)  
    # 线性求和
    def score(self, hidden, encoder_outputs):
        energy = self.attn(encoder_outputs)
        return torch.sum(hidden*energy,dim=2)

#Decoder层
class Decoder(nn.Module):
    def __init__(self, output_dim, embedding_dim, hidden_dim, num_layers=2, dropout=0.2):
        super().__init__()

        self.embedding_dim = embedding_dim
        self.hid_dim = hidden_dim
        self.output_dim = output_dim
        self.num_layers = num_layers
        self.dropout = dropout

        self.embedding = nn.Embedding(output_dim, embedding_dim)
        # 添加Attention
        self.attention = Attention(hidden_dim)
        self.rnn = nn.GRU(embedding_dim + hidden_dim, hidden_dim,
                          num_layers=num_layers, dropout=dropout)
        self.out = nn.Linear(embedding_dim + hidden_dim * 2, output_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, input, hidden, encoder_outputs):
        input = input.unsqueeze(0)
        embedded = self.dropout(self.embedding(input))
        #print(embedded.shape)
        attn_weight = self.attention(hidden, encoder_outputs)
        #print(attn_weight.shape)
        context = attn_weight.unsqueeze(1).bmm(encoder_outputs.transpose(0, 1)).transpose(0, 1)
        emb_con = torch.cat((embedded, context), dim=2)
        _, hidden = self.rnn(emb_con, hidden)
        output = torch.cat((embedded.squeeze(0), hidden[-1], context.squeeze(0)), dim=1)
        output = F.log_softmax(self.out(output), 1)
        return output, hidden, attn_weight
#组成seq2seq结构
class Seq2Seq(nn.Module):
    def __init__(self, encoder, decoder, device, teacher_forcing_ratio=0.5):
        super().__init__()

        self.encoder = encoder
        self.decoder = decoder
        self.device = device
        self.teacher_forcing_ratio = teacher_forcing_ratio

    def forward(self, src_seqs, src_lengths, trg_seqs):
        batch_size = src_seqs.shape[1]
        max_len = trg_seqs.shape[0]
        trg_vocab_size = self.decoder.output_dim
        
        outputs = torch.zeros(max_len, batch_size, trg_vocab_size).to(self.device)
        encoder_outputs, hidden = self.encoder(src_seqs, src_lengths)
        output = trg_seqs[0, :]
        for t in range(1, max_len): 
            output, hidden, _ = self.decoder(output, hidden, encoder_outputs)
            outputs[t] = output
            teacher_force = random.random() < self.teacher_forcing_ratio
            output = (trg_seqs[t] if teacher_force else output.max(1)[1])
        return outputs

    def predict(self, src_seqs, src_lengths, max_trg_len=20, start_ix=1):
        max_src_len = src_seqs.shape[0]
        batch_size = src_seqs.shape[1]
        trg_vocab_size = self.decoder.output_dim
        outputs = torch.zeros(max_trg_len, batch_size, trg_vocab_size).to(self.device)
        encoder_outputs, hidden = self.encoder(src_seqs, src_lengths)
        output = torch.LongTensor([start_ix] * batch_size).to(self.device)
        attn_weights = torch.zeros((max_trg_len, batch_size, max_src_len))
        for t in range(1, max_trg_len):
            output, hidden, attn_weight = self.decoder(output, hidden, encoder_outputs)
            outputs[t] = output
            output = output.max(1)[1]
            attn_weights[t] = attn_weight
        return outputs, attn_weights
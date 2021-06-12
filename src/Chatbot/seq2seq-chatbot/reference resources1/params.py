# -*- coding: utf-8 -*-

class Params:
	'''
	Parameters of our model
	'''
	src_train = "data/test/cutQ_train.txt"
	tgt_train = "data/test/cutA_train.txt"
	src_test = "data/test/cutQ_valid.txt"
	tgt_test = "data/test/cutA_valid.txt"
	enc_vocab = 'test_en.vocab.tsv'
	dec_vocab = 'test_de.vocab.tsv'

	batch_size = 2
	embedding_dim = 100
	hidden_dim = 100
	clip = 5
	num_epochs = 1   
	logdir = 'logdir'

    #a最大长度
	max_trg_len = 30
	num_identical = 6
	num_heads = 8
	dropout = 0.1

	word_limit_size = 20
	word_limit_lower = 3
	checkpoint = 'checkpoint'
    

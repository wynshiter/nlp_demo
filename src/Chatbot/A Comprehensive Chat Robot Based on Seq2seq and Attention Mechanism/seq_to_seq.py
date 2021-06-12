# -*- coding:utf-8 -*-
import numpy as np
import tensorflow as tf
from tensorflow import layers
from tensorflow.python.ops import array_ops
from tensorflow.contrib import seq2seq
from tensorflow.contrib.seq2seq import BahdanauAttention, LuongAttention, AttentionWrapper, BeamSearchDecoder
from tensorflow.contrib.rnn import LSTMCell, GRUCell, MultiRNNCell, DropoutWrapper, ResidualWrapper

from word_sequence import WordSequence
from data_utils import _get_embed_device


class Seq2Seq(object):
    """
    基本流程
    __init__ 基本参数保存，参数验证
    build_model 构建模型
    init_placeholder 初始化一些TensorFlow变量的占位符
    build_encoder 初始化编码器
        初始化单个解码器
        初始化解码单元

    init_optimizer 初始化训练优化器
    train 训练一个batch数据
    predict 预测一个batch数据
    """

    def __init__(self,
                 input_vocab_size,
                 target_vocab_size,
                 batch_size=32,
                 embedding_size=300,
                 mode='train',
                 hidden_size=256,
                 depth=1,
                 beam_width=0,
                 cell_type='lstm',
                 dropout=0.2,
                 use_dropout=False,
                 use_residual=False,
                 optimizer='adam',
                 learning_rate=1e-3,
                 min_learning_rate=1e-6,
                 decay_step=50000,
                 max_gradient_norm=5.0,
                 max_decode_step=None,
                 attention_type='Bahdanau',
                 bidirection=False,
                 time_major=False,
                 seed=0,
                 parallel_iterations=None,
                 share_embedding=False,
                 pretrained_embedding=False):
        """
        :param input_vocab_size: 输入词表大小
        :param target_vocab_size: 输出词表大小
        :param batch_size: batch大小
        :param embedding_size: 输入输出词表嵌入维度
        :param mode: 取之为train,表示训练模式，取之为decode，代表预训练模式
        :param hidden_size: RNN模型中间层大小，Encoder和Decoder层相同
        :param depth: rnn层数
        :param beam_width: beansearch超参数，用于解码
        :param cell_type: rnn神经元类型，lstm， gru等
        :param dropout: 随机丢弃比例， 0到1之间取值
        :param use_dropout: 是否用dropout
        :param use_residual: 是否使用residual
        :param optimizer: 使用哪一个优化器
        :param learning_rate: 学习率
        :param min_learning_rate: 最小学习率
        :param decay_step: 衰减步骤
        :param max_gradient_norm: 梯度正则裁剪系数
        :param max_decode_step: 最大decode长度，可以非常大
        :param attention_type: 使用attention类型
        :param bidirection:是否双向encoder
        :param time_major: 是否在计算过程中使用时间作为主要大批量数据
        :param seed: 一些层间操作大随机数
        :param parallel_iterations: 并行执行RNN循环的个数
        :param share_embedding:是否让encoder和decoder共用embedding
        :param pretrained_embedding: 是否使用预训练的embedding
        """
        self.input_vocab_size = input_vocab_size
        self.target_vocab_size = target_vocab_size
        self.batch_size = batch_size
        self.embedding_size = embedding_size
        self.mode = mode
        self.hidden_size = hidden_size
        self.depth = depth

        self.cell_type = cell_type.lower()
        self.dropout = dropout
        self.keep_prob = 1.0 - dropout
        self.use_dropout = use_dropout
        self.use_residual = use_residual
        self.optimizer = optimizer
        self.learning_rate = learning_rate
        self.min_learning_rate = min_learning_rate
        self.decay_step = decay_step
        self.max_gradient_norm = max_gradient_norm

        self.attention_type = attention_type
        self.bidirection = bidirection
        self.time_major = time_major
        self.seed = seed

        if isinstance(parallel_iterations, int):
            self.parallel_iterations = parallel_iterations
        else:
            self.parallel_iterations = batch_size

        self.share_embedding = share_embedding
        self.pretrained_embedding = pretrained_embedding

        # 生成均匀分布的随机数。
        self.initializer = tf.random_uniform_initializer(-0.05, 0.05, dtype=tf.float32)
        assert self.cell_type in ('gru', 'lstm'), 'cell_type应该是 GRU 或者 LSTM'
        if share_embedding:
            assert input_vocab_size == target_vocab_size, '如果share_embedding为True，那么两个vocab_size必须相同'
        assert mode in ('train', 'decode'), 'mode必须是train或者是decode'
        assert 0.0 <= dropout < 1.0, 'dropout必须大于等于0小于等于1'
        assert attention_type.lower() in ('bahdanau', 'luong'), 'attention_type 必须是bahdanau或者是luong'
        assert beam_width < target_vocab_size, "beam_width {} 应该小于target vocab {}".format(beam_width, target_vocab_size)

        self.keep_prob_placeholdle = tf.placeholder(tf.float32, shape=[], name='keep_prob')
        self.global_step = tf.Variable(0, trainable=False, name='global_step')
        self.use_beamsearch_decode = False
        self.beam_width = beam_width
        self.use_beamsearch_decode = True if self.beam_width > 0 else False
        self.max_decode_step = max_decode_step

        assert self.optimizer.lower() in (
            'adadelta', 'adam', 'rmsprop', 'momentum', 'sgd'), 'optimizer 必须是下列之一：adadelta, adam, rmsprop, momentum,sgd'
        self.build_mode()

    def build_mode(self):
        """
        1、初始化训练，预测所需要的变量
        2、构建编码器 encoder build_encoder -> encoder_cell -> build_single_cell
        3、构建解码器 decoder
        4、构建优化器 optimizer
        5、保存
        :return:
        """
        self.init_placeholder()
        encoder_outputs, encoder_state = self.build_encoder()
        self.build_decoder(encoder_outputs, encoder_state)

        if self.mode == 'train':
            self.init_optimizer()

        self.saver = tf.train.Saver()

    def init_optimizer(self):
        """
        sgd, adadelta, adam, rmsprop, momentum
        :return:
        """
        learning_rate = tf.train.polynomial_decay(
            self.learning_rate,
            self.global_step,
            self.decay_step,
            self.min_learning_rate,
            power=0.5
        )

        self.current_learning_rate = learning_rate

        # 返回需要训练参数的列表
        trainable_params = tf.trainable_variables()
        # 设置优化器
        if self.optimizer.lower() == 'adadelta':
            self.opt = tf.train.AdadeltaOptimizer(
                learning_rate=learning_rate
            )
        elif self.optimizer.lower() == 'adam':
            self.opt = tf.train.AdamOptimizer(
                learning_rate=learning_rate
            )
        elif self.optimizer.lower() == 'rmsprop':
            self.opt = tf.train.RMSPropOptimizer(
                learning_rate=learning_rate
            )
        elif self.optimizer.lower() == 'momentum':
            self.opt = tf.train.MomentumOptimizer(
                learning_rate=learning_rate
            )
        elif self.optimizer.lower() == 'sgd':
            self.opt = tf.train.GradientDescentOptimizer(
                learning_rate=learning_rate
            )
        gradients = tf.gradients(self.loss, trainable_params)
        # 梯度裁剪
        clip_gradients, _ = tf.clip_by_global_norm(
            gradients, self.max_gradient_norm
        )
        # 更新model
        self.update = self.opt.apply_gradients(
            zip(clip_gradients, trainable_params),
            global_step=self.global_step
        )

        gradients = tf.gradients(self.loss_rewards, trainable_params)
        clip_gradients, _ = tf.clip_by_global_norm(
            gradients, self.max_gradient_norm
        )
        self.updates_rewards = self.opt.apply_gradients(
            zip(clip_gradients, trainable_params),
            global_step=self.global_step
        )

        # 添加self.loss_add 的update
        gradients = tf.gradients(self.add_loss, trainable_params)
        clip_gradients, _ = tf.clip_by_global_norm(
            gradients, self.max_gradient_norm)
        self.updates_add = self.opt.apply_gradients(
            zip(clip_gradients, trainable_params),
            global_step=self.global_step)

    def save(self, sess, save_path='model.ckpt'):
        """
        保存格式两种：
        ckpt：保存所有的训练参数，尺寸相对比较大，可以用来进行模型的恢复和加载
        pb：用于模型最后的上线部署
        :param sess:
        :param save_path:
        :return:
        """
        self.saver.save(sess, save_path=save_path)

    def load(self, sess, save_path='model.ckpt'):
        print('try load model from ', save_path)
        self.saver.restore(sess, save_path)

    def init_placeholder(self):
        """
        :return:
        """
        self.add_loss = tf.placeholder(
                                       dtype=tf.float32,
                                       name="add_loss")

        self.encoder_inputs = tf.placeholder(
                                            dtype=tf.int32,
                                            shape=(self.batch_size, None),
                                            name='encoder_inputs')

        self.encoder_inputs_length = tf.placeholder(
                                                    dtype=tf.int32,
                                                    shape=(self.batch_size,),
                                                    name='encoder_inputs_length')

        if self.mode == 'train':
            #解码器的输入
            self.decoder_inputs = tf.placeholder(
                dtype=tf.int32,
                shape=(self.batch_size, None),
                name='decoder_inputs'
            )
            #解码器输入的rewards
            self.rewards = tf.placeholder(
                dtype=tf.float32,
                shape=(self.batch_size, 1),
                name='rewards'
            )
            #解码器的长度输入
            self.decoder_inputs_length = tf.placeholder(
                dtype=tf.int32,
                shape=(self.batch_size,),
                name='decoder_inputs_length'
            )

            self.decoder_start_token = tf.ones(
                shape=(self.batch_size, 1),
                dtype=tf.int32
            ) * WordSequence.START
            #实际训练时解码器的输入
            self.decoder_inputs_train = tf.concat([
                self.decoder_start_token,
                self.decoder_inputs
            ], axis=1)

    def build_single_cell(self, n_hidden, use_residual):
        '''
        构建一个单独的rnn 的cell
        :param n_hidden: 隐藏层的神经元数量
        :param use_residual: 是否使用 residual wrapper
        :return:
        '''
        if self.cell_type == 'gru':
            cell_type = GRUCell
        else:
            cell_type = LSTMCell

        cell = cell_type(n_hidden)

        if self.use_dropout:
            cell = DropoutWrapper(
                cell,
                dtype=tf.float32,
                output_keep_prob=self.keep_prob_placeholdle,
                seed=self.seed
            )

        if use_residual:
            cell = ResidualWrapper(cell)

        return cell

    def build_encoder_cell(self):
        '''
        构建单独的编码器
        :return:
        '''
        return MultiRNNCell([
            self.build_single_cell(
                self.hidden_size,
                use_residual=self.use_residual
            )
            for _ in range(self.depth)
        ])

    def build_encoder(self):
        """
        构建编码器
        :return:
        """
        with tf.variable_scope('encoder'):
            encoder_cell = self.build_encoder_cell()

            with tf.device(_get_embed_device(self.input_vocab_size)):

                if self.pretrained_embedding:

                    self.encoder_embeddings = tf.Variable(
                        tf.constant(0.0,
                                    shape=(self.input_vocab_size, self.embedding_size)),
                        trainable=True,
                        name='embeddings')

                    self.encoder_embeddings_placeholder = tf.placeholder(tf.float32,
                                                                         (self.input_vocab_size, self.embedding_size)
                                                                         )

                    self.encoder_embeddings_init = self.encoder_embeddings.assign(self.encoder_embeddings_placeholder)

                else:
                    self.encoder_embeddings = tf.get_variable(name='embeddings',
                                                              shape=(self.input_vocab_size, self.embedding_size),
                                                              initializer=self.initializer,
                                                              dtype=tf.float32)

            self.encoder_inputs_embedded = tf.nn.embedding_lookup(
                params=self.encoder_embeddings,
                ids=self.encoder_inputs)

            if self.use_residual:
                self.encoder_inputs_embedded = layers.dense(self.encoder_inputs_embedded,
                                                            self.hidden_size,
                                                            use_bias=False,
                                                            name='encoder_residual_projection')

            inputs = self.encoder_inputs_embedded
            if self.time_major:
                inputs = tf.transpose(inputs, (1, 0, 2))

            if not self.bidirection:
                (
                    encoder_outputs,
                    encoder_state
                ) = tf.nn.dynamic_rnn(
                                    cell=encoder_cell,
                                    inputs=inputs,
                                    sequence_length=self.encoder_inputs_length,
                                    dtype=tf.float32,
                                    time_major=self.time_major,
                                    parallel_iterations=self.parallel_iterations,
                                    swap_memory=True)
            else:
                # 双向rnn 多了合并操作
                encoder_cell_bw = self.build_encoder_cell()
                (
                    (encoder_fw_outputs, encoder_bw_outputs),
                    (encoder_fw_state, encoder_bw_state)
                ) = tf.nn.bidirectional_dynamic_rnn(
                    cell_bw=encoder_cell_bw,
                    cell_fw=encoder_cell,
                    inputs=inputs,
                    sequence_length=self.encoder_inputs_length,
                    dtype=tf.float32,
                    time_major=self.time_major,
                    parallel_iterations=self.parallel_iterations,
                    swap_memory=True)

                encoder_outputs = tf.concat(
                    (encoder_bw_outputs, encoder_fw_outputs), 2)

                encoder_state = []
                for i in range(self.depth):
                    encoder_state.append(encoder_fw_state[i])
                    encoder_state.append(encoder_bw_state[i])
                encoder_state = tuple(encoder_state)

        return encoder_outputs, encoder_state

    def build_decoder_cell(self, encoder_outputs, encoder_state):
        """
        构建解码器cell
        :param encoder_outputs:
        :param encoder_state:
        :return:
        """
        encoder_input_length = self.encoder_inputs_length
        batch_size = self.batch_size

        if self.bidirection:
            encoder_state = encoder_state[-self.depth:]

        if self.time_major:
            encoder_outputs = tf.transpose(encoder_outputs, (1, 0, 2))

        if self.use_beamsearch_decode:
            # 复制多份
            encoder_outputs = seq2seq.tile_batch(
                encoder_outputs, multiplier=self.beam_width
            )
            encoder_state = seq2seq.tile_batch(
                encoder_state, multiplier=self.beam_width
            )
            encoder_input_length = seq2seq.tile_batch(
                self.encoder_inputs_length, multiplier=self.beam_width
            )
            #如果使用了beamsearch,那么输入应该是beam_width的倍数于 batch_size的
            batch_size *= self.beam_width

        if self.attention_type.lower() == 'luong':
            self.attention_mechanism = LuongAttention(
                num_units=self.hidden_size,
                memory=encoder_outputs,
                memory_sequence_length=encoder_input_length
            )
        else:
            self.attention_mechanism = BahdanauAttention(
                num_units=self.hidden_size,
                memory=encoder_outputs,
                memory_sequence_length=encoder_input_length
            )

        cell = MultiRNNCell([
            self.build_single_cell(
                self.hidden_size,
                use_residual=self.use_residual)
            for _ in range(self.depth)
        ])

        alignment_history = (
            self.mode != 'train' and not self.use_beamsearch_decode
        )

        def cell_input_fn(inputs, attention):
            '''
            根据attn_input_feeding 属性来判断是否在attention计算前进行一次投影计算
            :param inputs:
            :param attention:
            :return:
            '''
            if not self.use_residual:
                return array_ops.concat([inputs, attention], -1)

            attn_projection = layers.Dense(self.hidden_size,
                                           dtype=tf.float32,
                                           use_bias=False,
                                           name='attention_cell_input_fn')
            return attn_projection(array_ops.concat([inputs, attention], -1))

        cell = AttentionWrapper(
                                cell=cell,
                                attention_mechanism=self.attention_mechanism,
                                attention_layer_size=self.hidden_size,
                                alignment_history=alignment_history,
                                cell_input_fn=cell_input_fn,
                                name='Attention_Wrapper'
        )

        decoder_initial_state = cell.zero_state(
            batch_size, tf.float32)

        # 传递encoder状态
        decoder_initial_state = decoder_initial_state.clone(
            cell_state=encoder_state
        )

        return cell, decoder_initial_state

    def build_decoder(self, encoder_outputs, encoder_state):
        '''
        构建解码器
        :param encoder_outputs:
        :param encoder_state:
        :return:
        '''


        with tf.variable_scope('decoder') as decoder_scope:
            (
                self.decoder_cell,
                self.decoder_initial_state
            ) = self.build_decoder_cell(encoder_outputs, encoder_state)
            #解码器的 embedding
            with tf.device(_get_embed_device(self.target_vocab_size)):
                if self.share_embedding:
                    self.decoder_embeddings = self.encoder_embeddings
                elif self.pretrained_embedding:

                    self.decoder_embeddings = tf.Variable(
                        tf.constant(0.0, shape=(self.target_vocab_size, self.embedding_size)),
                        trainable=True,
                        name='embeddings'
                    )

                    self.decoder_embeddings_placeholder =\
                        tf.placeholder(tf.float32, (self.target_vocab_size,
                                                    self.embedding_size))

                    self.decoder_embeddings_init = self.decoder_embeddings.assign(self.decoder_embeddings_placeholder)
                else:
                    self.decoder_embeddings = tf.get_variable(
                        name='embedding',
                        shape=(self.target_vocab_size, self.embedding_size),
                        initializer=self.initializer,
                        dtype=tf.float32
                    )

            self.decoder_output_projection = layers.Dense(self.target_vocab_size,
                                                          dtype=tf.float32,
                                                          use_bias=False,
                                                          name='decoder_output_projection')

            if self.mode == 'train':
                self.decoder_inputs_embdedded = tf.nn.embedding_lookup(
                    params=self.decoder_embeddings,
                    ids=self.decoder_inputs_train
                )

                inputs = self.decoder_inputs_embdedded

                if self.time_major:
                    inputs = tf.transpose(inputs, (1, 0, 2))

                training_helper = seq2seq.TrainingHelper(
                    inputs=inputs,
                    sequence_length=self.decoder_inputs_length,
                    time_major=self.time_major,
                    name='training_helper'
                )

                training_decoder = seq2seq.BasicDecoder(
                    cell=self.decoder_cell,
                    helper=training_helper,
                    initial_state=self.decoder_initial_state
                )

                max_decoder_length = tf.reduce_max(
                    self.decoder_inputs_length
                )

                (
                    outputs,
                    self.final_state,
                    _
                ) = seq2seq.dynamic_decode(
                    decoder=training_decoder,
                    output_time_major=self.time_major,
                    impute_finished=True,
                    maximum_iterations=max_decoder_length,
                    parallel_iterations=self.parallel_iterations,
                    swap_memory=True,
                    scope=decoder_scope
                )

                self.decoder_logits_train = self.decoder_output_projection(
                    outputs.rnn_output
                )

                self.masks = tf.sequence_mask(
                    lengths=self.decoder_inputs_length,
                    maxlen=max_decoder_length,
                    dtype=tf.float32,
                    name='masks'
                )

                decoder_logits_train = self.decoder_logits_train
                if self.time_major:
                    decoder_logits_train = tf.transpose(decoder_logits_train, (1, 0, 2))

                self.decoder_pred_train = tf.argmax(
                    decoder_logits_train, axis=-1, name='decoder_pred_train'
                )

                self.train_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
                    labels=self.decoder_inputs,
                    logits=decoder_logits_train)

                self.masks_rewards = self.masks * self.rewards

                self.loss_rewards = seq2seq.sequence_loss(
                    logits=decoder_logits_train,
                    targets=self.decoder_inputs,
                    weights=self.masks_rewards,
                    average_across_timesteps=True,
                    average_across_batch=True
                )

                self.loss = seq2seq.sequence_loss(
                    logits=decoder_logits_train,
                    targets=self.decoder_inputs,
                    weights=self.masks,
                    average_across_timesteps=True,
                    average_across_batch=True
                )

                self.add_loss = self.loss + self.add_loss

            elif self.mode == 'decode':
                start_token = tf.tile(
                    [WordSequence.START],
                    [self.batch_size]
                )
                end_token = WordSequence.END

                def embed_and_input_proj(inputs):
                    return tf.nn.embedding_lookup(
                        self.decoder_embeddings,
                        inputs
                    )

                if not self.use_beamsearch_decode:
                    decoder_helper = seq2seq.GreedyEmbeddingHelper(
                        start_tokens=start_token,
                        end_token=end_token,
                        embedding=embed_and_input_proj
                    )

                    inference_decoder = seq2seq.BasicDecoder(
                        cell=self.decoder_cell,
                        helper=decoder_helper,
                        initial_state=self.decoder_initial_state,
                        output_layer=self.decoder_output_projection
                    )
                else:
                    inference_decoder = BeamSearchDecoder(
                        cell=self.decoder_cell,
                        embedding=embed_and_input_proj,
                        start_tokens=start_token,
                        end_token=end_token,
                        initial_state=self.decoder_initial_state,
                        beam_width=self.beam_width,
                        output_layer=self.decoder_output_projection
                    )
                if self.max_decode_step is not None:
                    max_decoder_step = self.max_decode_step
                else:
                    max_decoder_step = tf.round(tf.reduce_max(
                        self.encoder_inputs_length
                    ) * 4)
                (
                    self.decoder_outputs_decode,
                    self.final_state,
                    self.final_sequence_lengths
                ) = (seq2seq.dynamic_decode(
                    decoder=inference_decoder,
                    output_time_major=self.time_major,
                    maximum_iterations=max_decoder_step,
                    parallel_iterations=self.parallel_iterations,
                    swap_memory=True,
                    scope=decoder_scope
                ))

                if not self.use_beamsearch_decode:
                    dod = self.decoder_outputs_decode
                    self.decoder_pred_decode = dod.sample_id

                    self.decoder_pred_decode = tf.transpose(
                        self.decoder_pred_decode, (1, 0)
                    )
                else:
                    self.decoder_pred_decode = self.decoder_outputs_decode.predicted_ids

                    if self.time_major:
                        self.decoder_pred_decode = tf.transpose(
                            self.decoder_pred_decode, (1, 0, 2)
                        )
                    self.decoder_pred_decode = tf.transpose(
                        self.decoder_pred_decode,
                        perm=[0, 2, 1]
                    )
                    dod = self.decoder_outputs_decode
                    self.beam_prob = dod.beam_search_decoder_output.scores

    def check_feeds(self, encoder_inputs, encoder_inputs_length,
                    decoder_inputs, decoder_inputs_length, decode):
        """

        :param encoder_inputs: 一个整型的二维矩阵，[batch_size, max_source_time_steps]
        :param encoder_inputs_length: [batch_size], 每一个维度是encoder句子的真实长度
        :param decoder_inputs: 一个整型的二维矩阵，[batch_size, max_target_time_steps]
        :param decoder_inputs_length: [batch_size], 每一个维度是decoder句子的真实长度
        :param decode: 是训练模式train(decode=False), 还是预测模式decode(decode=True)
        :return: TensorFlow所需的input_feed
        """
        input_batch_size = encoder_inputs.shape[0]
        if input_batch_size != encoder_inputs_length.shape[0]:
            raise ValueError('encoder_inputs 和 encoder_inputs_length的第一个维度必须一致',
                             "这个维度是batch_size, %d != %d" %
                             (input_batch_size, encoder_inputs_length.shape[0]))
        if not decode:
            target_batch_size = decoder_inputs.shape[0]
            if target_batch_size != input_batch_size:
                raise ValueError('encoder_inputs 和 decoder_inputs的第一个维度必须一致',
                                 "这个维度是batch_size, %d != %d" %
                                 (input_batch_size,target_batch_size))
            if target_batch_size != decoder_inputs_length.shape[0]:
                raise ValueError('decoder_inputs 和 decoder_inputs_length的第一个维度必须一致',
                                 "这个维度是batch_size, %d != %d" %
                                 (target_batch_size, decoder_inputs_length.shape[0]))

        input_feed = {self.encoder_inputs.name: encoder_inputs,
                      self.encoder_inputs_length.name: encoder_inputs_length}

        if not decode:
            input_feed[self.decoder_inputs.name] = decoder_inputs
            input_feed[self.decoder_inputs_length.name] = decoder_inputs_length

        return input_feed

    def train(self, sess, encoder_inputs, encoder_inputs_length,
              decoder_inputs, decoder_inputs_length, rewards=None,
              return_lr=False, loss_only=False, add_loss=None):
        """
        训练模型
        :param sess:
        :param encoder_inputs:
        :param encoder_inputs_length:
        :param decoder_inputs:
        :param decoder_inputs_length:
        :param rewards:
        :param return_lr:
        :param loss_only:
        :param add_loss:
        :return:
        """
        # 输入
        input_feed = self.check_feeds(encoder_inputs, encoder_inputs_length,
                                      decoder_inputs, decoder_inputs_length,
                                      False)
        # 设置dropout
        input_feed[self.keep_prob_placeholdle.name] = self.keep_prob

        if loss_only:
            # 输出
            return sess.run(self.loss, input_feed)

        if add_loss is not None:
            input_feed[self.add_loss.name] = add_loss
            output_feed = [
                self.updates_add, self.add_loss,
                self.current_learning_rate]
            _, cost, lr = sess.run(output_feed, input_feed)

            if return_lr:
                return cost, lr

            return cost

        if rewards is not None:
            input_feed[self.rewards.name] = rewards
            output_feed = [
                self.updates_rewards, self.loss_rewards,
                self.current_learning_rate
            ]
            _, cost, lr = sess.run(output_feed, input_feed)

            if return_lr:
                return cost, lr

            return cost

        output_feed = [
            self.update, self.loss,
            self.current_learning_rate
        ]
        _, cost, lr = sess.run(output_feed, input_feed)

        if return_lr:
            return cost, lr

        return cost

    def predict(self, sess,
                encoder_inputs,
                encoder_inputs_length,
                attention=False):
        # 输入
        input_feed = self.check_feeds(encoder_inputs, encoder_inputs_length,
                                      None, None, True)
        input_feed[self.keep_prob_placeholdle.name] = 1.0

        if attention:
            assert not self.use_beamsearch_decode, 'Attention模式不能打开 BeamSearch'
            pred, atten = sess.run([
                self.decoder_pred_decode,
                self.final_state.alignment_history.stack()
            ], input_feed)

            return pred, atten

        if self.use_beamsearch_decode:
            pred, beam_prob = sess.run([
                self.decoder_pred_decode, self.beam_prob
            ], input_feed)
            beam_prob = np.mean(beam_prob, axis=1)

            pred = pred[0]

            return pred

        pred, = sess.run([self.decoder_pred_decode], input_feed)

        return pred

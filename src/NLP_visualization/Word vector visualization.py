#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
'''
@Author  :   {SEASON}
@License :   (C) Copyright 2013-2022, {OLD_IT_WANG}
@Contact :   {shiter@live.cn}
@Software:   PyCharm
@File    :   NLP_DEMO -- Word vector visualization
@Time    :   2020/9/18 0:44
@Desc    :

参考：https://zhuanlan.zhihu.com/p/194263854

tensorboard 可视化：
https://zhuanlan.zhihu.com/p/33786815
使用bert-serving生成词向量并聚类可视化：
https://zhuanlan.zhihu.com/p/110655509

word2vec词向量可视化聚类与Bert词向量可视化聚类对比：
https://zhuanlan.zhihu.com/p/114390048

spacy 插件 ：
https://spacy.io/universe/project/whatlies
'''
#-------------------------------------------------------------------------------
import gensim

from sklearn.decomposition import IncrementalPCA    # 用于最初的降维
from sklearn.manifold import TSNE                   # 用于最终的降维
import numpy as np                                  # 用于数组控制
from plotly.offline import init_notebook_mode, iplot, plot
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import seaborn as sns
#%matplotlib inline
plt.rcParams['font.sans-serif']=['SimHei']  #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False    #用来正常显示负号


def reduce_dimensions(model, plot_in_notebook=True):
    fig, ax = plt.subplots(figsize=(30, 30))
    num_dimensions = 2  # 最终的维度数（2维、3维等）
    vectors = []  # 向量空间中的位置
    labels = []  # “跟踪”词汇以便稍后再次标记我们的数据

    for word in list(model.wv.vocab)[:50]:  # 鉴于模型中的4000+词汇，进行可视化的话会耗费大量的计算时间和计算资源，所以笔者仅展示TOP 300词汇
        vectors.append(model.wv[word])
        labels.append(word)  # 将两个列表转换为numpy向量以进行降维

    vectors = np.asarray(vectors)
    labels = np.asarray(labels)  # 使用t-SNE进行降维
    vectors = np.asarray(vectors)
    # logging.info - 这个网站可出售。 - 最佳的Logging 来源和相关信息。('即将开始t-SNE降维处理。这可能会花费些时间...')
    tsne = TSNE(n_components=num_dimensions, n_iter=250, metric='euclidean', random_state=2019)
    vectors = tsne.fit_transform(vectors)
    x_vals = [v[0] for v in vectors]
    y_vals = [v[1] for v in vectors]  # 创建一个 trace
    trace = go.Scatter(x=x_vals, y=y_vals, mode='text', text=labels)
    data = [trace]
  # logging.info - 这个网站可出售。 - 最佳的Logging 来源和相关信息。('词嵌入可视化图谱绘制已经完成！')
    if plot_in_notebook:
      init_notebook_mode(connected=True)
      iplot(data, filename='word-embedding-plot')
    else:
      plot(data, filename='word-embedding-plot.html')





def main():
    model = gensim.models.Word2Vec.load('../word2vector/gensim_temp.txt')
    print(len(model.wv.vocab))

    #reduce_dimensions(model, plot_in_notebook=False)



if __name__=="__main__":
    main()


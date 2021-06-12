# encoding: utf-8
'''
@author: season
@contact: shiter@live.cn

@file: visualization.py
@time: 2019/1/20 22:48
@desc: 可视化相关代码

参考：
https://segmentfault.com/a/1190000012394176
探索性数据分析：
https://www.jianshu.com/p/9325c9f88ee6
'''




import sys
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

###-----以下导入 其他文件夹的包


from Database import mySQLiteForblog,blog
import character_processing_tool




CURRENT_URL = os.path.dirname(__file__)
PARENT_URL = os.path.abspath(os.path.join(CURRENT_URL, os.pardir))
sys.path.append(PARENT_URL)



#可以使用pandas read_sql
def database_to_pandas_dataframe(str_path_sqlite):
    '''

    :param str_path_sqlite:  # sql_order is a string
    :return:
    '''

    try:
        conn = sqlite3.connect(str_path_sqlite)
        str_sql = '''select * from CSDN_Blog'''
        frame = pd.read_sql(str_sql, conn, index_col=None, coerce_float=True, params=None, parse_dates=None, columns=None,
                 chunksize=None)

        return  frame
    except Exception as e:
        print(e)

def add_feature_for_blog(dataframe):
    '''
    将文章内容分割，中文一列，英文字符一列，增加中文字数，英文字数，总字数
    :param dataframe: 从sqlite 中查出所有列，放在pandas dataframe 中
    :return:
    '''
    dataframe['content'] = dataframe['content'].astype(str)
    dataframe['中文'] = dataframe['content'].apply(character_processing_tool.get_all_chinese_string_and_punctuation)
    dataframe['英文'] = dataframe['content'].apply(character_processing_tool.get_all_english_word)
    dataframe['中文字数'] = dataframe['中文'].apply(len)
    dataframe['英文字数'] = dataframe['英文'].apply(len)

    return  dataframe

def huizhixiaoshi(dataframe):
    '''
    绘制博客发布所在小时的直方图
    :param dataframe:
    :return:
    test1 = dataframe.groupby(["create_time_hour"]).count()
    '''

    dataframe["博客发布时间统计"] = dataframe["article_id"].apply(lambda x: 1)
    dataframe_fenbu  = dataframe.groupby(["create_time_hour"])["博客发布时间统计"].count().reset_index()
    dataframe_fenbu = dataframe_fenbu.sort_values(by=["博客发布时间统计"], ascending=False)


    sns.set_style('whitegrid', {'font.sans-serif': ['SimHei', 'Arial']})
    sns.set_context("talk")


    fig, axes = plt.subplots(figsize=(15, 15))
    #
    ax = sns.barplot(x=dataframe_fenbu.create_time_hour, y=dataframe_fenbu.博客发布时间统计, palette='Blues_d')
    ax.set_ylabel("博客发表小时分布")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=-90)
    plt.show()

def yuanchuang_zhuanzai(dataframe):
    '''
    用distplot 看分布应该是连续的变量
    :param dataframe:
    :return:
    '''
    dataframe["博客发布时间统计"] = dataframe["article_id"].apply(lambda x: 1)
    dataframe_yuanchuangfenbu = dataframe[dataframe['article_type']=='原'].groupby(["create_time_hour"])["博客发布时间统计"].count().reset_index()
    dataframe_yuanchuangfenbu = dataframe_yuanchuangfenbu.sort_values(by=["create_time_hour"], ascending=False)

    dataframe_zhuanzai_fenbu = dataframe[dataframe['article_type']=='转'].groupby(["create_time_hour"])["博客发布时间统计"].count().reset_index()
    dataframe_zhuanzai_fenbu = dataframe_zhuanzai_fenbu.sort_values(by=["create_time_hour"], ascending=False)

    sns.set_style('whitegrid', {'font.sans-serif': ['SimHei', 'Arial']})
    sns.set_context("talk")
    # 创建图表
    fig = plt.figure(figsize=(12, 12))
    plt.subplots_adjust(hspace=0.3)

    ax0 = fig.add_subplot(2,1,1)
    ax1 = fig.add_subplot(2,1,2)


    ax0.set_title(u"原创发表时间分布")
    ax1.set_title(u"转载发表时间分布")
    sns.distplot(dataframe_yuanchuangfenbu['博客发布时间统计'],color='#86AFCB',bins=1,rug=True,ax=ax0)
    sns.distplot(dataframe_zhuanzai_fenbu['博客发布时间统计'],color='#99bcda',bins=1,rug=True,ax=ax1)

    plt.show()

def main():
    '''
    主函数
    :return:
    '''

    str_path_sqlite = r'../Database/NLP_demo.db'

    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)
    # 设置value的显示长度为100，默认为50
    pd.set_option('max_colwidth', 100)
    dataframe = database_to_pandas_dataframe(str_path_sqlite)
    dataframe = add_feature_for_blog(dataframe)
    #huizhixiaoshi(dataframe)
    yuanchuang_zhuanzai(dataframe)
    print(dataframe.head(1))

if __name__ == '__main__':
    main()
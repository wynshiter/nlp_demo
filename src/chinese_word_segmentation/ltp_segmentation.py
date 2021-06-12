# encoding: utf-8
'''
@author: season
@contact: shiter@live.cn

@file: chinese_word _segmentation.py
@time: 2018/11/27 10:33
@desc: pyltp 分词样例程序

由于pyltp 不支持conda  环境，故本 repo 没有安装及相关实验

'''



#pyltp 使用文档
#https://pyltp.readthedocs.io/zh_CN/latest/api.html

# ltp 模型下载链接 哈工大语言云官网
# http://ltp.ai/download.html

#安装 报错，调试方法：
#https://blog.csdn.net/weixin_40899194/article/details/79702468


import os
from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from pyltp import Parser
from pyltp import SementicRoleLabeller
import re


#pyltp官方文档http://pyltp.readthedocs.io/zh_CN/develop/api.html#id15
#http://blog.csdn.net/MebiuW/article/details/52496920
#http://blog.csdn.net/lalalawxt/article/details/55804384

LTP_DATA_DIR =  r'D:\code\python\csdn_nlp\ltp_data_v3.4.0'  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
srl_model_path = os.path.join(LTP_DATA_DIR, 'pisrl_win.model')  # 语义角色标注模型目录路径，注意windows 和linux 使用不同模型
print("======================>>>>"+srl_model_path)




# 分句，也就是将一片文本分割为独立的句子
def sentence_splitter(sentence='你好，你觉得这个例子从哪里来的？当然还是直接复制官方文档，然后改了下这里得到的。我的微博是MebiuW，转载请注明来自MebiuW！'):
    sents = SentenceSplitter.split(sentence)  # 分句
    print('\n'.join(sents))


"""分词"""
def segmentor(sentence=None):
    try:
        segmentor = Segmentor()  # 初始化实例
        segmentor.load(cws_model_path)  # 加载模型
        words = segmentor.segment(sentence)  # 分词
    #默认可以这样输出
    #print ('\t'.join(words))
    # 可以转换成List 输出
        words_list = list(words)
        segmentor.release()  # 释放模型
        return words_list
    except Exception as e:
        print(e)
        return ''
    finally:
        pass


"""词性标注"""
def posttagger(words):


    postagger = Postagger() # 初始化实例
    postagger.load(pos_model_path)  # 加载模型
    postags = postagger.postag(words)  # 词性标注
    for word,tag in zip(words,postags):
        print(word+'/'+tag)
    postagger.release()  # 释放模型
    return postags


"""命名实体识别"""
def ner(words,postags):
    print('命名实体开始')
    recognizer = NamedEntityRecognizer()
    recognizer.load(ner_model_path) #加载模型
    netags = recognizer.recognize(words,postags) #命名实体识别
    for word,ntag in zip(words,netags):
        print(word+'/'+ ntag)
    recognizer.release()   #释放模型
    nerttags = list(netags)
    return nerttags

"""依法"""
def parse(words, postags):
    parser = Parser() # 初始化实例
    parser.load(par_model_path)  # 加载模型
    arcs = parser.parse(words, postags)  # 句法分析
    print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
    parser.release()  # 释放模型
    return arcs


def role_label(words, postags, netags, arcs):
    labeller = SementicRoleLabeller() # 初始化实例
    labeller.load(srl_model_path)  # 加载模型
    #roles = labeller.label(words, postags, netags, arcs)  # 语义角色标注
    roles = labeller.label(words, postags, arcs)
    for role in roles:
        print(str(role.index)+"".join(
            ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))
    labeller.release()  # 释放模型
    return roles

# def testss():
#     sentence="600251后市怎样操作？谢谢。"
#     hagongdaLTP=pyltpT.PyltpT()
#     hagongdalist = hagongdaLTP.ltpmain(sentence)
#     sentence1="$精华制药(sz003买入，短线还有机会吗？压力位多少，大概什么价位卖掉合适？谢谢。"
#     hagongdaLTP1 = pyltpT.PyltpT()
#     hagongdalist2 = hagongdaLTP1.ltpmain(sentence1)
#     print(hagongdalist)
#     for item in hagongdalist2:
#         if 'sh' or 'sz' in item:
#             hagongdalist2[hagongdalist2.index(item)]=item[2:8]
#         item = re.sub("[\s+\.\!\/_,\[\]：$\-:);%；=^*(+\"\']+|[+——\“！\”，?。？<《》>、~@#￥%……&*（）]+", '', item)
#         if len(item)==1:
#             hagongdalist2.remove(item)
#     print(hagongdalist2)







#
# def hagongda2(sentence):
#     LTP_DATA_DIR = 'E:\BaiduNetdiskDownload\ltp_data_v3.4.0'  # ltp模型目录的路径
#     cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
#     cidian_path = os.path.join(LTP_DATA_DIR, 'cidian.txt')
#     print(cidian_path)
#     segmentor = Segmentor()  # 初始化实例
#     segmentor.load_with_lexicon(cws_model_path, cidian_path)  # 加载模型
#     sentence = ''.join(sentence.split())
#     sentence = re.sub("[\s+\.\!\/_,\[\]：$\-:);%；=^*(+\"\']+|[+——\“！\”，?。？<《》>、~@#￥%……&*（）]+", '', sentence)
#     words = segmentor.segment(sentence)
#     #print(' '.join(words))
#     words_list = list(words)
#     segmentor.release()
#     return words_list




# def test():
#     project_path = r"..\..\ltp_data_v3.4.0"  # 项目文件夹目录
#     # 可设置ltp_test、（cws、pos、par、ner）_cmdline，但是注意各自能用的参数，没有的参数请置空""
#     model_exe = "cws_cmdline"  # 又如cws_cmdline
#
#     threads_num = " --threads " + str(3)  # 更改线程数
#     #last_stage = " --last-stage " + "all"  # 最终步骤，可设置ws、pos、ner、dp、srl、all
#     input_path = " --input " + "test.txt"  # 输入文件
#     seg_lexicon = ""  # 分词用户词典
#     pos_lexicon = ""  # 词性标注用户词典
#     output_path = "out.txt"  # 输出文件
#
#     command = "cd " + project_path + " & " + model_exe + threads_num + input_path + " > " + output_path
#     os.system(command)



# def main():
#     #sentence_splitter()
#     words = segmentor('我家在中科院，我现在在北京上学。中秋节你是否会想到李白？')
#     # print(words)
#     tags = posttagger(words)
#     netags=ner(words,tags)
#     arcs = parse(words,tags)
#     roles = role_label(words, tags, netags, arcs)
#
#     print(roles)
#

# if __name__ == '__main__':
#     main()




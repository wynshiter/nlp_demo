# encoding: utf-8
'''
@author: season
@contact: shiter@live.cn

@file: character_processing_tool.py
@time: 2019/3/11 16:18
@desc:对文本字符串进行一些操作，中文提取，英文提取等
汉字处理的工具:
判断unicode是否是汉字，数字，英文，或者其他字符。
全角符号转半角符号。
标点符号参考：https://www.cnblogs.com/arkenstone/p/6092255.html
其他写法：
判断是否是全数字：
        str.encode('UTF-8').isdigit()

 判断是否是全英文：
         str.encode('UTF-8').isalpha()

print "孙".encode('UTF-8').isdigit()
print "孙".encode('UTF-8').isalpha()
print '123few'.encode('UTF-8').isdigit()
print '123few'.encode('UTF-8').isalpha()
print '123'.encode('UTF-8').isdigit()
print 'few'.encode('UTF-8').isalpha()


汉字，汉语拼音提取：https://zhon.readthedocs.io/en/latest/#
这个库没有句号，不认为是一句话

'''


import os
import sys
import re
import zhon
import zhon.hanzi


CURRENT_URL = os.path.dirname(__file__)
PARENT_URL = os.path.abspath(os.path.join(CURRENT_URL, os.pardir))
sys.path.append(PARENT_URL)



#PUNCTUATION_STRING= r'''＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､　、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？｡。'''

UNICODECHINESESTRING = r'[\u4e00-\u9fff'+zhon.hanzi.punctuation+']'

def is_chinese(uchar):
    '''
    中文常用字符的范围是u'\u4e00' - u'\u9fff' 有的代码也用下面的这个
    判断一个unicode是否是汉字
    :param uchar:
    :return:
    '''
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


def is_number(uchar):
    '''
    判断一个unicode是否是数字
    :param uchar:
    :return:
    '''
    if uchar >= u'\u0030' and uchar <= u'\u0039':
        return True
    else:
        return False




def is_alphabet(uchar):
    '''
    判断一个unicode是否是英文字母
    :param uchar:
    :return:
    '''
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False

def get_all_english_string(temp_string):
    '''
    获取一个字符串的所有英文字符,包括空格
    :param temp_string:
    :return:
    '''
    unicodeEnglish = re.compile(r'[\u0041-\u005a\u0061-\u007a,\u0020]')
    english_string = "".join(unicodeEnglish.findall(temp_string))
    return  english_string

def get_all_chinese_string(temp_string):
    '''
    获取一个字符串的所有中文字,不包括标点
    :param temp_string:
    :return:
    '''
    unicodeChinese = re.compile(r'[\u4e00-\u9fff]')
    chinese_string = "".join(unicodeChinese.findall(temp_string))
    return  chinese_string

def get_all_chinese_string_and_punctuation(temp_string):
    '''
    获取一个字符串的所有中文字以及中文标点
    :param temp_string:
    :return:
    '''

    unicodeChinese = re.compile(UNICODECHINESESTRING)
    chinese_string_list = re.findall(unicodeChinese, temp_string)
    return   "".join(chinese_string_list)

def contents_other_than_chinese_characters(temp_str):
    '''
    获取到除去汉字字符以外的内容（仅针对中英混合），这样可以获取到夹杂在中文中的英文
    首先将中文及中文标点替换为空格，再将多个空格替换为一个
    :param temp_str:
    :return:
    '''
    unicodeChinese = re.compile(UNICODECHINESESTRING)

    nonChineseString = re.sub(unicodeChinese, " ", temp_str)
    nonChineseString = re.sub(' +', ' ', nonChineseString)
    return nonChineseString

def get_all_english_word(temp_str):
    '''
    获取多语言中文档中的英文单词字符串，含有空格
    :param temp_str:
    :return:
    '''
    temp_str = contents_other_than_chinese_characters(temp_str)


    return get_all_english_string(temp_str).lower()


def is_other(uchar):
    '''
    判断是否是（汉字，数字和英文字符之外的）其他字符
    :param uchar:
    :return:
    '''
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return True
    else:
        return False


def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += chr(inside_code)
    return rstring


def strB2Q(ustring):
    """半角转全角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 32:  # 半角空格直接转化
            inside_code = 12288
        elif inside_code >= 32 and inside_code <= 126:  # 半角字符（除空格）根据关系转化
            inside_code += 65248

        rstring += chr(inside_code)
    return rstring


def convert_toUnicode(string):
    '''
    """将UTF-8编码转换为Unicode编码"""
    :param string:
    :return:
    '''
    ustring = string
    if not isinstance(string, str):
        ustring = string.decode('UTF-8')
    return ustring


if __name__ == "__main__":

    ustring1 = u'收割季节 麦浪和月光 洗着快镰刀'
    string1 = 'Sky0天地Earth1*'
    string2 = "China's Legend Holdings will split its several business arms to go public on stock markets, " \
              "the group's president Zhu Linan said on Tuesday." \
              "该集团总裁朱利安周二表示，中国联想控股将分拆其多个业务opencv部门in在股市上市。我了歌曲: ： 这样不行？；‘“”’ "

    ustring1 = convert_toUnicode(ustring1)
    string1 = convert_toUnicode(string1)
    print(strB2Q(string2))
    print(get_all_english_string(string2))
    print(get_all_english_word(string2))
    # print(get_all_chinese_string(string2))
    # print(get_all_chinese_string_and_punctuation(string2))
    # print(len(get_all_chinese_string_and_punctuation(string2)))
    # print(zhon.hanzi.punctuation)
    print(contents_other_than_chinese_characters(string2))
    print(len(contents_other_than_chinese_characters(string2)))
    # for item in string1:
    #     print(is_chinese(item))
    #     print(is_number(item))
    #     print(is_alphabet(item))
    #     print(is_other(item))


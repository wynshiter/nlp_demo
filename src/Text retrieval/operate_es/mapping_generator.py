#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
'''
@Author  :   {SEASON}
@License :   (C) Copyright 2013-2022, {OLD_IT_WANG}
@Contact :   {shiter@live.cn}
@Software:   PyCharm
@File    :   NLP_DEMO -- mapping_generator
@Time    :   2020/9/30 20:53
@Desc    :

按照数据类型，自动生成es 的mapping
'''
#-------------------------------------------------------------------------------


import json
# 按照每一列的类型生成对应的 es index


def set_mapper_field_text(list_name, s_type, mapper,text_analyzer,text_search_analyzer):
    '''
    自动生成mapping json，尤其针对text 字段指定分词方式。
    '''
    mapper_json = json.loads(json.dumps(mapper))
    for item in list_name:
        mapper_json['properties'][item] = {"type": s_type}
        if s_type == 'text':
            mapper_json['properties'][item]["analyzer"] = text_analyzer
            mapper_json['properties'][item]["search_analyzer"] = text_search_analyzer

    return mapper_json

def set_mapper_field(list_name, s_type, mapper):
    '''
    自动生成mapping json，尤其针对text 字段指定分词方式。
    '''
    mapper_json = json.loads(json.dumps(mapper))
    for item in list_name:
        mapper_json['properties'][item] = {"type": s_type}

    return mapper_json

# medicine_insurance_mapper = json.loads(create_medicine_insurance_body)


# 生成一个字典 进行字段对应


# create_medicine_insurance_body = {
#     "properties": {
#
#     }
# }

### 简单的将 数值型 与字符型调出来
# e.g.
# dict_mapper = set_mapper_field(FloatType_list, 'float', create_medicine_insurance_body)
# dict_mapper = set_mapper_field(IntegerType_list, 'integer', dict_mapper)
# dict_mapper = set_mapper_field(category_list, 'keyword', dict_mapper)
# dict_mapper = set_mapper_field(str_list, 'keyword', dict_mapper)
#
# json_mapper = json.dumps(dict_mapper, ensure_ascii=False)
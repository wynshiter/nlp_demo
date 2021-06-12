#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
'''
@Author  :   {SEASON}
@License :   (C) Copyright 2013-2022, {OLD_IT_WANG}
@Contact :   {shiter@live.cn}
@Software:   PyCharm
@File    :   apolo -- load_datafile_to_elasticsearch_settings
@Time    :   2019/12/6 15:46
@Desc    :

'''
#-------------------------------------------------------------------------------

es_ip = ''
es_port = '9200'
ES_INDEX = 'disease'
ES_TYPE = 'doc'
BULK_SZIE = 500

# DISEASE_CHINESE_NAME = ["疾病名称","主要编码","附加编码","一级编码","二级编码","三级编码","四级编码","一级描述","二级描述","三级描述","四级描述"]
#
#
# DISEASE_ENGLISH_NAME = ["iz_disease_code","disease_name", "main_code", "additional_code", "code_level1", "code_level2", "code_level3", "code_level4",
#            "description_level1", "description_level2", "description_level3", "description_level4"]

DISEASE_ENGLISH_NAME = ['code','main_code','add_code','name']

create_disease_body = {
    "properties": {
        "code": {
            "type": "keyword"
        },
        "main_code": {
            "type": "keyword"
        },
        "add_code": {
            "type": "keyword"
        },
        "name": {
            "type": "text",
            "analyzer": "hanlp_standard",
            "search_analyzer": "hanlp_speed"
        }


    }
}

HOSPITAL_CHINESE_COLUMN=[]
HOSPITAL_ENGLISH_COLUMN=['code','circ_code','name','alias','province','city','county','address','phone','zipcode','home_url','type','grade']
create_hospital_body = {
    "properties": {
        "code": {
            "type": "keyword"
        },
        "circ_code": {
            "type": "keyword"
        },
        "name": {
            "type": "text",
            "analyzer": "hanlp_standard",
            "search_analyzer": "hanlp_speed"
        },
        "alias": {
            "type": "text",
            "analyzer": "hanlp_standard",
            "search_analyzer": "hanlp_speed"
        },
        "province": {
            "type": "keyword"
        },
        "city": {
            "type": "keyword"
        },
        "county": {
            "type": "keyword"
        },
        "address": {
            "type": "text",
            "analyzer": "hanlp_standard",
            "search_analyzer": "hanlp_speed"
        },
        "phone": {
            "type": "keyword"
        },
        "zipcode": {
            "type": "keyword"
        },
        "home_url": {
            "type": "keyword"
        },
        "type": {
            "type": "keyword"
        },
        "grade": {
            "type": "keyword"
        }
    }
}




body = {
    "properties": {
        "name": {
            "type": "text",
            "analyzer": "hanlp_standard",
            "search_analyzer": "hanlp_speed"
        }
    }
}

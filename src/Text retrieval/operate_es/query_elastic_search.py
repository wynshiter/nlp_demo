#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
'''
@Author  :   {SEASON}
@License :   (C) Copyright 2013-2022, {OLD_IT_WANG}
@Contact :   {shiter@live.cn}
@Software:   PyCharm
@File    :   apolo -- query_elastic_search
@Time    :   2019/12/4 16:44
@Desc    :

'''
#-------------------------------------------------------------------------------


common = {
  "ES_settings": {
    "host_addr": "172.31.8.56",
    "port": 9200
  },
  "request_size": 20
}

ES = common.ES
request_size = common.REQUEST_SIZE


def generate_query_body(value):
    body = {
        "query": {
            "match": {
                "medical_product_name": value
            }
        },
        "size": request_size
    }
    return body


def gen_query_med(name):
    body = {
        "query": {
            "match": {
                "medical_product_name": name
            }
        },
        "size": request_size
    }
    return body


def gen_query_hos(name):
    body = {
        "query": {
            "match": {
                "hospital_name": name
            }
        },
        "size": request_size
    }
    return body


def is_not_blank(s):
    if (s == None) | (s == ""):
        return False
    else:
        return True


def get_condition(name, mainCode, additionalCode):
    name_condition = {"match": {"disease_name": name}}
    mainCode_condition = {"match": {"main_code": mainCode}}
    add_condition = {"match": {"additional_code": additionalCode}}
    conditions = []
    if is_not_blank(name):
        conditions.append(name_condition)
    if is_not_blank(mainCode):
        conditions.append(mainCode_condition)
    if is_not_blank(additionalCode):
        conditions.append(add_condition)
    return conditions


def gen_query_disease(name, mainCode, additionalCode):
    conditions = get_condition(name, mainCode, additionalCode)

    print(conditions)
    body = {
        "query": {
            "bool": {
                "must": conditions,
            }
        }
    }
    return body




def query_med_data(index, name):
    # query data from index medicine
    query_body = gen_query_med(name)
    print(query_body)

    data = []
    msg = "request data succeed"

    try:
        res = ES.search(index=index, body=query_body)
        for hit in res['hits']['hits']:
            src = hit["_source"]
            record = {
                "medical_product_name": src["medical_product_name"],
                "general_product_name": src["general_product_name"],
                "english_name": src["english_name"],
                "formula": src["formula"],
                "specification": src["specification"],
                "manufacturing_unit": src["manufacturing_unit"],
                "product_type": src["product_type"],
                "drug_standard_number": src["drug_standard_number"],
                "approval_number": src["approval_number"]
            }
            data.append(record)
        response = {
            "total": len(data),
            "data": data,
            "msg": msg
        }
    except:
        response = common.SearchFailed_response
    return response


def query_disease_data(index, name, mainCode, additionalCode):
    # query data from index disease
    query_body = gen_query_disease(name, mainCode, additionalCode)
    print(query_body)
    data = []
    msg = "request data succeed"
    try:
        res = ES.search(index=index, body=query_body)
        print(res)
        for hit in res['hits']['hits']:
            src = hit["_source"]
            record = {
                "disease_name": src["disease_name"],
                "main_code": src["main_code"],
                "additional_code": src["additional_code"]
            }
            data.append(record)
        response = {
            "total": len(data),
            "data": data,
            "msg": msg
        }
    except:
        response = common.SearchFailed_response
    return response


def query_hospital_data(index, name):
    # query data from index hospital
    query_body = gen_query_hos(name)

    data = []
    msg = "request data succeed"
    try:
        res = ES.search(index=index, body=query_body)
        for hit in res['hits']['hits']:
            src = hit["_source"]
            record = {
                "hospital_name": src["hospital_name"],
                "hospital_grade": src["hospital_grade"],
                "province_code": src["province_code"],
                "city_code": src["city_code"],
                "area_district": src["area_district"],
                "address": src["address"]
            }
            data.append(record)
        response = {
            "total": len(data),
            "data": data,
            "msg": msg
        }
    except Exception as e:
        print(e)
        response = common.SearchFailed_response
    return response

from es_search.Deal_res import deal_res
import requests
'''
（1）本文件为后端请求发送部分，其中send_post向es数据库发送请求，通过改变data中的参数来改变访问的索引和查询方式，返回re_num代表返回的最大数量，re_id代表返回的形式，
传入参数s为查询语句
（2）send_neo_post为向neo4j数据库发送请求，其中参数s为查询语句
'''


def send_post(s):
    url = 'http://119.8.116.2:5602/quicksearch'
    data = {
        'index': 'new-open',
        'keywords': s,
        'operator_str': 'or',
        'query_way': 'match',
        're_id': 3,
        're_num': 3,
        'ik_way': 'ik_max_word'
    }
    response = requests.post(url, data=data)
    result = response.json()
    res_num = result['num']
    res = result['results']
    if res_num == 1:
        res = deal_res(res['hits']['hits'], data['re_num'], data['re_id'])
    print(res)
    return res_num, res


def send_neo_post(s):
    url = 'http://124.71.97.70:5606/neo_search'
    data = {
        'string': s
    }
    response = requests.post(url, data=data)
    result = response.json()
    res_num = result['nums']
    res = result['results']
    return res_num, res




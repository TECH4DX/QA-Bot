# coding:utf-8
from py2neo import Node, Relationship, Graph, Path, Subgraph
from py2neo import NodeMatcher, RelationshipMatcher
import jieba
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from Model_train_predict.example.ner.standard.search_predict import search_pre
from flask import Flask, request
app = Flask(__name__)
import json

'''
本文档为进行neo4j数据库查询的后端文件，可以直接部署在服务器相应端口上，通过修改url、usr、key、table_name来把对应的数据库表修改为自己的
数据库表，同时内置了查询语句，只需要从前端获取到查询语句即可，修改后可直接在服务器运行
'''

@app.route('/neo_search', methods=['post'])   #返回序号：0代表返回空，1代表返回成功，2代表发生neo4j数据库链接查询异常，3说明模型预测异常
def neo_data_search():
    #提取参数
    res_data = request.form
    s = res_data['string']
    ##连接neo4j数据库，输入地址、用户名、密码
    url = 'http://119.8.116.2:5603'
    usr = 'neo4j'
    key = '980819'
    key_words = []  # 最终得到的关键词字典
    table_name = 'Euler'        #neo4j数据库表名称
    try:
        graph = Graph(url, auth=(usr, key))
    except:
        return json.dumps({'nums': 2, 'results': key_words})
    node_matcher = NodeMatcher(graph)
    relationship_matcher = RelationshipMatcher(graph)
    #############################################################
    relation_list = ['安装', '工具安装', '上面安装', '编译安装', '进行安装', '输入', '使用安装', '参考', '版本', '版本号', '创建或使用关联', '使用参考', '使用']
    relation_cut_list = []
    s_list = jieba.cut_for_search(s)
    str_list = list(s_list)
    for i in str_list:
        str = ''
        for j in relation_list:
            if i in j and j not in relation_cut_list:
                if str == '':
                    str = j
                else:
                    if i == j:
                        str = j
        if str != '':
            relation_cut_list.append(str)
    ##############################################
    try:
        res = search_pre(s)
    except:
        return json.dumps({'nums': 3, 'results': key_words})
    #如果并没有命名体识别出结果，直接返回代码0和空列表，由前端送入ES查找
    if len(res) == 0:
        return json.dumps({'nums': 0, 'results': key_words})
    else:
        try:
            for i in res:
                key_words.append(i)
                if len(relation_cut_list) != 0:
                    for j in relation_cut_list:
                        s = "'" + i + "'"
                        cypher1 = "MATCH (n:" + table_name + ")-[r:" + j + "]->(m:" + table_name + ") WHERE n.name=" + s + " RETURN m.name AS name"
                        df = graph.run(cypher1).to_data_frame()
                        if not df.empty:
                            for l in df['name']:
                                key_words.append(l)
                        cypher2 = "MATCH (n:" + table_name + ")-[r:" + j + "]->(m:" + table_name + ") WHERE m.name=" + s + " RETURN n.name AS name"
                        df2 = graph.run(cypher2).to_data_frame()
                        if not df2.empty:
                            for l in df2['name']:
                                key_words.append(l)

                #else:
                #    relationship = list(relationship_matcher.match([node1], r_type=None))
                #   nums = 0
                #   for k in relationship:
                #       nums = nums + 1
                #       if nums > 20:
                #            break
                #       key_words.append(k.end_node['name'])
        except:
            return json.dumps({'nums': 2, 'results': list()})
    return json.dumps({'nums': 1, 'results': key_words})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5606)
                






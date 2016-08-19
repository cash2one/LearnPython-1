# coding:utf-8
import jieba
from elasticsearch import Elasticsearch
import db.mysql_common
import config.mysql_config


def word():
    para_dict = config.mysql_config.get_config("../file/mysql_online.conf")

    mysql = db.mysql_common.MysqlCommon(para_dict['host'], para_dict['port'], para_dict['user'], para_dict['pwd'],
                                        para_dict['db'])
    count = mysql.fetch_count("select count(*) from npc_poi limit 2000");

    es = Elasticsearch(hosts='10.94.48.41:8200')

    for index in range(141000, count[0], 1000):
        print index

        names = mysql.fetch_data("select poi_id,poi_name from npc_poi limit " + str(index) + "," + str(index + 1000))
        data = []
        for name in names:
            json_data = {}
            json_data['poi_id'] = name[0]
            json_data['poi_name'] = name[1]
            seg_list = jieba.cut(name[1])
            json_data['poi_new_name'] = " ".join(seg_list)
            data.append(json_data)
        cache = []
        for d in data:
            new_action = {}
            new_action['_index'] = 'word'
            new_action['_type'] = 'word'
            new_action['_id'] = d['poi_id']
            action = {}
            action['index'] = new_action
            cache.append(action)
            cache.append(d)
        es.bulk(body=cache, index='word', doc_type='word')


if "__main__" == __name__:
    word()

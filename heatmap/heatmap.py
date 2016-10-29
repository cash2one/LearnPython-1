# coding:utf-8
from elasticsearch import Elasticsearch

import datetime, time


def heatmap():
    file = open("d:\\000002_0")
    data = []
    i = 0
    es = Elasticsearch(hosts='10.94.48.41:8200')
    for line in file:
        i += 1
        cols = line.split("\n")[0].split("\t")
        json_data = {}
        json_data['firm_id'] = long(cols[0])
        json_data['uid'] = long(cols[1])
        json_data['deal_id'] = long(cols[2])
        json_data['cert_id'] = long(cols[3])
        json_data['location'] = str(float(cols[5]) / 10000) + "," + str(float(cols[4]) / 10000)
        s = datetime.datetime(2016, 8, 1, 0, 0, 0)
        result = time.mktime(s.timetuple())
        json_data['day'] = long(result * 1000)
        data.append(json_data)
        if i >= 1000:
            cache = []
            for d in data:
                new_action = {}
                new_action['_index'] = 'heatmap'
                new_action['_type'] = 'heatmap'
                new_action['_id'] = d['cert_id']
                action = {}
                action['index'] = new_action
                cache.append(action)
                cache.append(d)
            result = es.bulk(body=cache, index='heatmap', doc_type='heatmap')
            print result
            data = []
            i = 0


if "__main__" == __name__:
    heatmap()

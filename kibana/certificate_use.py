# coding:utf-8
from elasticsearch import Elasticsearch

import os
import time
import threading
import datetime as dt
from datetime import datetime


def certificate_use(dir, month, day):
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        file = open(path)
        data = []
        i = 0
        es = Elasticsearch(hosts='10.94.48.41:8200')
        for line in file:
            i += 1
            cols = line.split("\n")[0].split("\t")
            json_data = {}
            try:
                json_data['deal_id'] = long(cols[0], 0)
                json_data['current_price'] = long(cols[1])
                json_data['simple_price'] = long(cols[1]) / 10000 * 10000
                json_data['single_price'] = long(cols[2])
                json_data['use_time'] = str(cols[3])
                json_data['firm_id'] = long(cols[4])
                json_data['location'] = str(float(cols[6]) / 10000) + "," + str(float(cols[5]) / 10000)
                json_data['area_id'] = long(cols[7])
                json_data['uid'] = long(cols[8])
                json_data['user_id'] = long(cols[9])
                json_data['mobile'] = long(cols[10])
                json_data['category_id_1'] = long(cols[11])
                json_data['category_name_1'] = str(cols[12]).decode('utf-8')
                json_data['category_id_2'] = long(cols[13])
                json_data['category_name_2'] = str(cols[14]).decode('utf-8')
                json_data['certificate_id'] = long(cols[15])
                json_data['cert_money'] = long(cols[16])
                s = dt.datetime(2016, month, day, 0, 0, 0)
                result = time.mktime(s.timetuple())
                json_data['day'] = long(result * 1000)
            except Exception as e:
                print e
                continue
            data.append(json_data)
            if i >= 1000:
                cache = []
                for d in data:
                    new_action = {}
                    new_action['_index'] = 'cert'
                    new_action['_type'] = 'cert_info'
                    new_action['_id'] = d['certificate_id']
                    action = {}
                    action['index'] = new_action
                    cache.append(action)
                    cache.append(d)
                result = es.bulk(body=cache, index='cert', doc_type='cert_info')
                # print result
                data = []
                i = 0
        print path


if "__main__" == __name__:
    rootDir = "D:\\cert\\cert"
    threads = []
    for dirs in os.listdir(rootDir):
        dir = os.path.join(rootDir, dirs)
        date = dirs.split("=")[1]
        d = datetime.strptime(date, '%Y%m%d')
        t = threading.Thread(name=date,
                             target=certificate_use, args=(dir, d.month, d.day))
        threads.append(t)

    for thread in threads:
        thread.start()

        # for thread in threads:
        #     thread.join()
        #     print 1

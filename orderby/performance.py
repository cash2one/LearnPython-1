import db.mysql_common as mysql
import config.mysql_config as config
import numpy as np
import matplotlib.pyplot as plt

__author__ = 'shangbin01'


def performance_pic():
    cate_para_dict = config.get_config("../file/mysql_common.conf")

    category_db = mysql.MysqlCommon(cate_para_dict['host'], cate_para_dict['port'], cate_para_dict['user'],
                                    cate_para_dict['pwd'],
                                    cate_para_dict['db'])
    categories = category_db.fetch_data("select id,name from category where parent_id<>0")

    dp_para_dict = config.get_config("../file/mysql_dp.conf")

    dp = mysql.MysqlCommon(dp_para_dict['host'], dp_para_dict['port'], dp_para_dict['user'], dp_para_dict['pwd'],
                           dp_para_dict['db'])
    for category in categories:
        sql = "select loaddate,sum(cert_count) from dp_deal_detail_performance_day_v1 where loaddate>=20160801 and loaddate<=20160814 and category_id_2=" + \
              str(category[0]) + " GROUP BY loaddate ORDER BY loaddate asc"
        results = dp.fetch_data(sql)
        dict = {}

        for result in results:
            dict[result[0]] = result[1]
        for i, key in enumerate(dict):  # Circulate both index and value(Here is key)
            plt.bar(i, dict[key], color='r', width=0.2)
        plt.xticks(np.arange(len(dict)) + 0.1, dict.keys())  # Translation
        plt.yticks(dict.values())
        plt.grid(True)
        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)
        print category[1].encode("utf-8")
        fig.savefig('d:\\del\\pic\\' + category[1].replace("/", "") + '.png', dpi=100)
        fig.clear()


if "__main__" == __name__:
    performance_pic()

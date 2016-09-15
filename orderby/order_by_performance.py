import db.mysql_common as mysql
import config.mysql_config as config
import numpy as np
import matplotlib.pyplot as plt


def performance_pic():
    dp_para_dict = config.get_config("../file/mysql_online.conf")

    dp = mysql.MysqlCommon(dp_para_dict['host'], dp_para_dict['port'], dp_para_dict['user'], dp_para_dict['pwd'],
                           dp_para_dict['databases'])
    while (True):
        category = input("category:")
        sql = "select loaddate,sum(cert_count) from dp_deal_detail_performance_day_v1 where loaddate>=20160801 and loaddate<=20160814 and category_id_2=" + category + " GROUP BY loaddate ORDER BY loaddate asc"
        results = dp.fetch_data(sql)
        data = {}
        for result in results:
            data[result[0]] = data[result[1]]
            plt.bar(result[0], result[1], color='r', width=0.2)
        plt.xticks(np.arange(len(data)) + 0.1, data.keys())  # Translation
        plt.yticks(data.values())
        plt.grid(True)
        plt.show()


if "__main__" == __name__:
    performance_pic()

import db.mysql_common as mysql
import config.mysql_config as config
import numpy as np
import matplotlib.pyplot as plt


def performance_pic():
    dp_para_dict = config.get_config("../file/mysql_online.conf")

    dp = mysql.MysqlCommon(dp_para_dict['host'], dp_para_dict['port'], dp_para_dict['user'], dp_para_dict['pwd'],
                           dp_para_dict['db'])

    common_para_dict = config.get_config("../file/mysql_online.conf")
    common = mysql.MysqlCommon(common_para_dict['host'], common_para_dict['port'], common_para_dict['user'],
                               common_para_dict['pwd'],
                               common_para_dict['db'])
    categories = common.fetch_data("select id from category where parent_id<>0")
    for category in categories:
        sql = "select deal_id,loaddate,sum(cert_count) " \
              "from dp_deal_detail_performance_day_v1 " \
              "where loaddate>=20160801 and loaddate<=20160814 and category_id_2=" + str(category) + \
              "group by loaddate,deal_id order by sum(cert_count) limit 10"
    while (True):
        pass


if "__main__" == __name__:
    performance_pic()

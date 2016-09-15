# coding:utf-8

import config.mysql_config as config
import databases.mysql_common as database


def export_firm_name_address():
    para_dict = config.get_config("../file/mysql_online.conf")

    mysql = database.MysqlCommon(para_dict['host'], para_dict['port'], para_dict['user'], para_dict['pwd'],
                                 para_dict['db'])
    count = mysql.fetch_count("select count(*) from npc_poi")

    file_name = open("D:\\tmp\\name", "w")
    file_address = open("D:\\tmp\\address", "w")

    for index in range(0, count[0], 1000):
        print index
        name_address = mysql.fetch_data(
            "select poi_name,address from npc_poi limit " + str(index) + "," + str(index + 1000))
        for data in name_address:
            file_name.write(data[0].encode("utf-8") + "\n")
            file_address.write(data[1] + "\n")

    file_name.close()
    file_address.close()


if "__main__" == __name__:
    export_firm_name_address()

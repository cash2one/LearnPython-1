import MySQLdb


def temp():
    try:
        conn = MySQLdb.connect(host="cp01-dba-baino04.cp01", port=8888, user="root", passwd="root", db="niux_crmv3",
                               charset="utf8")
        cur = conn.cursor()
        f = open("/Users/baidu/Downloads/supply.txt")
        sql = "insert into crm_supply_account_user_rela(account_id,account_name,creator_id)values(%s,%s,%s)"
        index = 0
        batchStr = []
        for line in f:
            index += 1
            batchStr.append(line.split(",")[0:3])
            if index == 1000:
                cur.executemany(sql, batchStr)
                conn.commit()
                index = 0
    except Exception as e:
        print e
    finally:
        conn.close()
        f.close()


if __name__ == "__main__":
    temp()

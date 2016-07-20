import MySQLdb

try:
    conn = MySQLdb.connect(host="10.48.54.40", port=8442, user="zhengtian", passwd="sW6q0Q70aW", db="niux_crmv3",
                           charset="utf8")
    cursor = conn.cursor()

    file = open("/Users/baidu/temp/a", 'w')

    cursor.execute("select count(*) from npc_poi_category_rela")
    count = cursor.fetchall()

    for index in range(0, count[0][0], 10000):

        n = cursor.execute("select poi.poi_id,poi.city_id,poi.poi_name,poi.description,"
                           "poi.district_id,poi.is_rival_checked,cate.category_id,deal.poi_deal_type,"
                           "deal.first_pay_start_time,deal.last_pay_end_time,visit.is_visit,visit.need_help,"
                           "visit.visit_process,rival.rival_new_deal,rival.rival_online,info.deal_num,"
                           "info.total_sale_amount,info.total_sale_amount_money,info.total_sale_amount_daily,"
                           "info.total_sale_amount_money_daily,info.last_month_cnt,info.last_month_turnover "
                           "from npc_poi_category_rela cate "
                           "left join npc_poi poi on cate.poi_id=poi.poi_id "
                           "left join npc_poi_deal_status_collect deal on poi.poi_id=deal.poi_id "
                           "left join npc_poi_visit_status_collect visit on poi.poi_id=visit.poi_id "
                           "left join npc_poi_rival_deal_status_collect rival on poi.poi_id=rival.poi_id "
                           "left join crm_firm_deal_info info on poi.poi_id=info.firm_id and site=0 "
                           "where poi.poi_id>0 limit " + str(index) + "," + str(index + 10000))
        for row in cursor.fetchall():
            print row
            line = str(row[0] * 3 + 1) + "\t" + str(row[1]) + "\t" + row[2].encode('utf-8') + "\t" + row[3].encode(
                'utf-8') + "\t" + str(row[4]) + "\t" + str(row[5]) + "\t" + str(row[6]) + "\t" + str(
                row[7]) + "\t" + str(
                row[8]) + "\t" + str(row[9]) + "\t" + str(row[10]) + "\t" + str(row[11]) + "\t" + str(
                row[12]) + "\t" + str(
                row[13]) + "\t" + str(row[14]) + "\t" + str(row[15]) + "\t" + str(row[16]) + "\t" + str(
                row[17]) + "\t" + str(row[18]) + "\t" + str(row[19]) + "\t" + str(row[20]) + "\t" + str(
                row[21]) + "\n"
            file.write(line)

except:
    Exception

finally:
    conn.close()
    file.close()

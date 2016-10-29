# coding:utf-8
import numpy as np
import pandas as pd
import os


def deal_user_file():
    file = open("C:\\Users\\sunbeansoft\\Downloads\\top_100")
    datas = np.array([0, 0, 0], dtype=np.long)

    for line in file:
        cols = line.split("\t")
        print cols
        new = np.array(cols, dtype=np.long)
        datas = np.vstack((datas, new))
    print datas


def deal_user_numpy():
    deal_user_type = np.dtype({'names': ['deal_id', 'u_id', 'cnt'], 'formats': ['f', 'f', 'f']})
    datas = np.loadtxt("C:\\Users\\sunbeansoft\\Downloads\\top_495424", delimiter="\t", dtype=deal_user_type)
    datas.g
    print datas


def deal_user_pandas():
    datas = pd.read_table("C:\\Users\\sunbeansoft\\Downloads\\top\\top_3783654.txt")
    datas.plot(kind='bar')
    result = datas.groupby("cnt").count()


def recreate_file():
    file = open("C:\\Users\\sunbeansoft\\Downloads\\top\\top_100")
    file_dic = {}

    for line in file:
        cols = line.split("\t")
        if file_dic.has_key(cols[0]):
            file = file_dic.get(cols[0])
            file.write(cols[0] + "\t" + cols[2])

        else:
            file = open("C:\\Users\\sunbeansoft\\Downloads\\top\\top_" + cols[0] + ".txt", mode='w')
            file.write("deal_id\tcnt\n")
            file.write(cols[0] + "\t" + cols[2])
            file_dic[cols[0]] = file
    for file in file_dic.values():
        file.close()


def deal_cnt():
    path = 'C:\\Users\\sunbeansoft\\Downloads\\top'
    for root, dirs, files in os.walk(path):
        for file in files:
            datas = pd.read_table(path + "\\" + file)
            datas.groupby("cnt").count()[:20].plot(kind='bar').figure.savefig(
                path + "\\" + file.replace(".txt", "") + ".png")


if __name__ == "__main__":
    deal_cnt()

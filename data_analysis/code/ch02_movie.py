# coding:utf-8

import pandas as pd

unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
mnames = ['movie_id', 'title', 'genres']

users = pd.read_table('D:\\fun\\github\\LearnPython\\data_analysis\\data\\users.dat', sep='::', header=None,
                      names=unames)
rating = pd.read_table('D:\\fun\\github\\LearnPython\\data_analysis\\data\\ratings.dat', sep='::', header=None,
                       names=rnames)
movies = pd.read_table('D:\\fun\\github\\LearnPython\\data_analysis\\data\\movies.dat', sep='::', header=None,
                       names=mnames)
data = pd.merge(pd.merge(rating, users), movies)
data.ix[0]

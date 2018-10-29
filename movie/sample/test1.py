# -*- coding: utf-8 -*-

import pandas as pd
import os
import operator

movies = pd.read_csv(r'/Users/swz/work/EOP/电影/data/douban电影1.csv',encoding = 'UTF-8')
#movie1 = movies[(movies.movie_name == '战狼2')]
#movie1 = movie1.append(movies[(movies.movie_name == '西虹市首富')])

#xx = movies[(movies.movie_name == 'xx')]
#if xx.empty:
#    print('none')
#else:
#    print(xx)
xx = '战狼2'
#movie1 = movies[(movies.movie_name == xx)]
#print(movie1)

os.chdir(r'/Users/swz/workspace/python/movie')
fp = open('mn.txt', 'r',encoding = 'UTF-8')
words = fp.readlines()
movie1 = movies[(movies.movie_name == 'xx')]
for word in words:
    print(word)
    print(operator.eq(xx,str(word)))
    temp = movies[(movies.movie_name == word)]
    if temp.empty:
        print('no has movie:'+word)
    else:
        movie1 = movie1.append(temp)

print(movie1.head(10))

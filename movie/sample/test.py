# -*- coding:utf-8 -*-

import re
import datetime
from pytesseract import *
from PIL import Image
import requests as req
from io import BytesIO
import traceback

#temp = '2018-09-24(分钟)'
#re.findall(r"\d+",temp)
#^([^\(]*)\(.*$
#print(re.findall(r'(^([^\(]*)\(.*$)',temp))
#regexp_extract(item_title,'《(.*?)(》)',1) as movie,
#regexp_extract(item_title,'》(.*?)(电影票)',1) as cinema,
#begin = datetime.date(2014,6,1)
#end = datetime.date(2014,7,7)
#for i in range((end - begin).days+1):
#    day = begin + datetime.timedelta(days=i)
#    print(str(day))
img_src = 'http://img.58921.com/sites/all/movie/files/protec/3f0d46693f97ce66947d317adaf35724.png'
response = req.get(img_src)
im = Image.open(BytesIO(response.content))
#im = Image.open('124.png')
#lang='eng' lang='chi_sim'
text = image_to_string(im,lang='chi_sim')
print(text)

temp = '伪恋OAD：丢失/巫女小姐 ニセコイ フンシツ/ミコサン'
try:
    temp = temp[0:temp.index(' ')]
except:
    traceback.print_exc()
print(temp)
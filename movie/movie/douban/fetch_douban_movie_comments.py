'''
Created on 2018年9月27日

@author: swz
'''
import requests 
import re
import pandas as pd
import time
import random

url_first='https://movie.douban.com/subject/27135550/comments?status=P'
head={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/59.0.3071.109 Chrome/59.0.3071.109 Safari/537.36'}
cookies={'cookie':'4XROJa7g9ts'}  #也就是找到你的账号对应的cookie
html=requests.get(url_first,headers=head,cookies=cookies)

reg=re.compile(r'<a href="(.*?)&amp;.*?class="next">') #下一页
ren=re.compile(r'<span class="votes">(.*?)</span>.*?comment">(.*?)</a>.*?</span>.*?<span.*?class="">(.*?)</a>.*?<span>(.*?)</span>.*?title="(.*?)"></span>.*?title="(.*?)">.*?class=""> (.*?)\n')  #评论等内容

#while html.status_code==200:
url_next='https://movie.douban.com/subject/27135550/comments'+re.findall(reg,html.text)[0]                             
wyzc=re.findall(ren,html.text)
data=pd.DataFrame(wyzc)
print(data)
data.to_csv('/Users/swz/workspace/python/movie/wyzc-comments.csv', header=False,index=False,mode='a+') #写入csv文件,'a+'是追加模式
data=[]
    #time.sleep(random.randint(1, 5))
    #html=requests.get(url_next,cookies=cookies,headers=head)
    #print(html.status_code)
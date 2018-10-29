'''
Created on 2018年9月20日

@author: swz
'''
import os
import time
import requests
from bs4 import BeautifulSoup
from _weakref import proxy

#num获取num页 国内高匿ip的网页中代理数据
def fetch_proxy(num):
    #修改当前工作文件夹
    os.chdir(r'/Users/swz/workspace/python/movie')
    #http://www.66ip.cn/
    api = 'http://www.xicidaili.com/nn/'
    header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/'
                  '537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    fp = open('host.txt', 'a+', encoding=('utf-8'))
    for i in range(num+1):
        #api = api.format(cnt=str(i))
        url = api+str(i)
        respones = requests.get(url=url, headers=header)
        soup = BeautifulSoup(respones.text, 'lxml')
        container = soup.find_all(name='tr',attrs={'class':'odd'})
        for tag in container:
            try:
                con_soup = BeautifulSoup(str(tag),'lxml')
                td_list = con_soup.find_all('td')
                ip = str(td_list[1])[4:-5]
                port = str(td_list[2])[4:-5]
                protocol = str(td_list[5]).replace('<td>', '').replace('</td>', '')
                #if protocol == 'HTTP':
                proxy = protocol+'://'+ip + ':' + port + '\n'
                fp.write(proxy)
            except Exception as e:
                print(e)
        time.sleep(1)
    fp.close()
    
fetch_proxy(10)
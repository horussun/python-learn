'''
Created on 2018年9月20日

@author: swz
'''
import os
import time
import requests
from bs4 import BeautifulSoup

def test_proxy():
    N = 1
    os.chdir(r'/Users/swz/workspace/python/movie')
    url = 'https://www.baidu.com'
    fp = open('host.txt', 'r')
    ips = fp.readlines()
    proxys = list()
    for p in ips:
        ip = p.strip('\n')
        proxy = 'http:\\' + ip
        proxies = {'proxy': proxy}
        proxys.append(proxies)
    for pro in proxys:
        try:
            s = requests.get(url, proxies=pro)
            print('第{}个ip：{} 状态{}'.format(N,pro,s.status_code))
        except Exception as e:
            print(e)
        N+=1
        
test_proxy()
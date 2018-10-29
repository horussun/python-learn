'''
Created on 2018年9月20日

@author: swz
'''
import os

#生成代理池子，num为代理池容量
def proxypool(num):
    os.chdir(r'/Users/swz/workspace/python/movie')
    fp = open('host.txt', 'r')
    proxys = list()
    ips = fp.readlines()
    for p in ips:
        #ip = p.strip('\n')
        proxy = p.strip('\n')
        proxies = {'proxy': proxy.lower()}
        proxys.append(proxies)
    return proxys

def proxypool_protocol(num):
    os.chdir(r'/Users/swz/workspace/python/movie')
    fp = open('host.txt', 'r')
    proxys = list()
    ips = fp.readlines()
    for p in ips:
        #ip = p.strip('\n')
        proxy = p.strip('\n')
        proxies = {proxy[0:proxy.find(':')].lower(): proxy.lower()}
        proxys.append(proxies)
    return proxys

print(proxypool(5))
# -*- coding: utf-8 -*-
'''
Created on 2018年9月20日

@author: swz
'''
import time
import random
import string
from movie.proxy.pool_proxy import proxypool,proxypool_protocol
import requests
import os
import csv
from lxml import etree
import json
import re
import traceback
    
def fetch_moives(tag,country,pages):
    os.chdir(r'/Users/swz/workspace/python/movie')
    csv_file = open("{}.csv".format(tag+'-'+country), 'a+', newline='', encoding='utf-8')
    writer = csv.writer(csv_file)
    writer.writerow(('movie_id', 'movie_name', 'director', 'actor', 'scriptwriter', 'runtime', 'genres', 'year', 'release_date', 'area', 'duoban_score', 'duoban_votes', 'duoban_comments', 'tags', 'abstract', 'movie_url', 'imdb_url', 'budget', 'revenue'))
    
    url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags={}&countries={}&start={}'
    for page in range(0, pages*(20+1), 20):
        
        headers = get_header()
        proxy = random.choice(proxypool_protocol(1))
        cookie = get_cookie()
        
        to_url = url.format(tag,country,page)
        print(to_url)
        print(proxy)
        try:
            #后续修改判定代理是否可用，如不可用在代理池里面删除
            response = requests.get(to_url, headers=headers, proxies=proxy,cookies=cookie,timeout=10)
            print(response.status_code)
            while response.status_code!=200:
                proxy = random.choice(proxypool_protocol(1))
                print('main proxy:')
                print(proxy)
                response = requests.get(to_url, headers=headers, proxies=proxy,cookies=cookie,timeout=10)
            #selector = etree.HTML(response.text)
            movies = json.loads(response.text)
            movies = movies['data']
            for movie in movies:
                detail_url = movie['url']
                print(detail_url)
                detail_response = requests.get(detail_url,headers=headers, proxies=proxy,cookies=cookie,timeout=10)
                while detail_response.status_code!=200:
                    proxy = random.choice(proxypool_protocol(1))
                    print('detail proxy:')
                    print(proxy)
                    detail_response = requests.get(detail_url,headers=headers, proxies=proxy,cookies=cookie,timeout=10)
                selector = etree.HTML(detail_response.text)
                try:
                    movie_id = detail_url[33:-1]
                    movie_name = selector.xpath('//span[@property="v:itemreviewed"]/text()')[0]
                    director = selector.xpath('//*[@rel="v:directedBy"]/text()')
                    actor = selector.xpath('//*[@rel="v:starring"]/text()')
                    scriptwriter = selector.xpath('//div[@id="info"]/span[2]/span[@class="attrs"]/a/text()')
                    runtime = ''
                    try:
                        runtime = re.findall(r"\d+",selector.xpath('//*[@property="v:runtime"]/text()')[0])[0]
                    except:
                        traceback.print_exc()
                    genres = selector.xpath('//*[@property="v:genre"]/text()')
                    year = selector.xpath('//*[@property="v:initialReleaseDate"]/text()')[0][0:4]
                    release_date = selector.xpath('//*[@property="v:initialReleaseDate"]/text()')[0][0:10]
                    #area = selector.xpath('//*[@property="v:initialReleaseDate"]/text()')[0][11:15]
                    area = selector.xpath('//*[@id="info"]').re('制片国家/地区:</span>\s(.*)<br>')
                    duoban_score = ''
                    try:
                        duoban_score = selector.xpath('//*[@property="v:average"]/text()')[0]
                    except:
                        traceback.print_exc()
                    duoban_votes = ''
                    try:
                        duoban_votes = selector.xpath('//*[@property="v:votes"]/text()')[0]
                    except:
                        traceback.print_exc()
                    duoban_comments = ''
                    tags = ''
                    try:
                        tags = selector.xpath('//div[@class="tags-body"]/a/text()')
                    except:
                        traceback.print_exc()
                    abstract = selector.xpath('//*[@property="v:summary"]/text()')[0]
                    imdb_url = ''
                    try:
                        imdb_url = 'http://www.imdb.com/title/'+selector.xpath('//div[@id="info"]/a[@rel="nofollow"]/text()')[0]
                    except:
                        traceback.print_exc()
                    budget = ''
                    revenue = ''
                    
                    writer.writerow((movie_id, movie_name, director, actor, scriptwriter, runtime, genres, year, release_date, area, duoban_score, duoban_votes, duoban_comments, tags, abstract, detail_url, imdb_url, budget, revenue))
                except:
                    traceback.print_exc()
                #time.sleep(1)
        except:
            traceback.print_exc()    
    csv_file.close()
    
def get_user_agent():
    user_agent_list = [
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 3.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; msn OptimizedIE8;ZHCN)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW6s4; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; Zune 4.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; OfficeLiveConnector.1.4; OfficeLivePatch.1.3; yie8)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; OfficeLiveConnector.1.3; OfficeLivePatch.0.0; Zune 3.0; MS-RTC LM 8)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; OfficeLiveConnector.1.3; OfficeLivePatch.0.0; MS-RTC LM 8; Zune 4.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8)',
    ]
    return user_agent_list

def get_num():
    return ''.join(random.sample(string.digits + string.ascii_letters, 11))

def get_cookie():
    return {'bid': get_num(), 'll': '"108296"'}

def get_header():
    return {
        'User-Agent': random.choice(get_user_agent())
    }

def main():
    start = time.time()
    #tags = input('请输入需要的类型，ex：电影、电视剧')
    #country = input('请输入需要的国家')
    #pages = input('请输入需要的页数')
    fetch_moives('电影','中国大陆',300)
    end = time.time()
    lastT = int(end-start)
    print('耗时{}s'.format(lastT))
    
if __name__ == '__main__':
    main()

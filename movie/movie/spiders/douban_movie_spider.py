'''
Created on 2018年9月20日

@author: swz
'''

from scrapy import Request
from scrapy.spiders import Spider
from movie.items import DoubanMovieItem
import json
import sys
import traceback
import time, random

#scrapy crawl douban_movie -o douban-cn.csv
class DoubanMovieSpider(Spider):
    name = 'douban_movie'
    #headers = {
    #    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    #}
    #dont_filter=True

    def start_requests(self):
        url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=电影&countries=英国&start='
        cnt = 0;
        #yield Request(url+str(cnt), headers=self.headers, meta={"cnt":cnt}, dont_filter=True)
        yield Request(url+str(cnt), meta={"cnt":cnt}, dont_filter=True)

    def parse(self, response):
        url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=电影&countries=英国&start='
        cnt = response.meta['cnt']
        cnt += 20;
        #9970
        if cnt > 1000:
            return None
        movies = json.loads(response.body_as_unicode())
        movies = movies['data']
        for movie in movies:
            time.sleep(random.uniform(1, 3))
            yield Request(movie['url'], callback=self.parse_detail, meta={'start_url':movie['url']}, dont_filter=True)
        yield Request(url+str(cnt), callback=self.parse, meta={"cnt":cnt}, dont_filter=True)
            
    def parse_detail(self, response):
        try:
            item = DoubanMovieItem()
            item['movie_url'] = response.meta['start_url']
            item['movie_id'] = response.meta['start_url'][33:-1]
            item['movie_name'] = response.xpath('//span[@property="v:itemreviewed"]/text()').extract()[0]
            try:
                item['movie_name'] = item['movie_name'][0:item['movie_name'].index(' ')]
            except:
                traceback.print_exc()
            item['director'] = response.xpath('//span/a[@rel="v:directedBy"]/text()').extract()
            try:
                item['scriptwriter'] = response.xpath('//div[@id="info"]/span[2]/span[@class="attrs"]/a/text()').extract()
            except:
                traceback.print_exc()
            item['actor'] = response.xpath('//*[@rel="v:starring"]/text()').extract()
            item['genres'] = response.xpath('//*[@property="v:genre"]/text()').extract()
            try:
                item['year'] = response.xpath('//*[@property="v:initialReleaseDate"]/text()').extract()[0][0:4]
            except:
                traceback.print_exc()
            try:
                #item['release_date'] = response.xpath('//*[@property="v:initialReleaseDate"]/text()').extract()[0][0:10]
                item['release_date'] = response.xpath('//*[@property="v:initialReleaseDate"]/text()').extract()
            except:
                traceback.print_exc()
            #item['area'] = response.xpath('//*[@property="v:initialReleaseDate"]/text()').extract()[0][11:15]
            try:
                item['area'] = response.xpath('//*[@id="info"]').re('制片国家/地区:</span>\s(.*)<br>')
            except:
                traceback.print_exc()
            try:
                item['runtime'] = response.xpath('//*[@property="v:runtime"]/text()').re(r'(\d+)')[0]
                #item['runtime'] = response.xpath('//*[@property="v:runtime"]/text()').re(r'(^([^\(]*)\(.*$)')[0]
            except:
                traceback.print_exc()
            try:
                item['imdb_url'] = 'http://www.imdb.com/title/'+response.xpath('//div[@id="info"]/a[@rel="nofollow"]/text()').extract()[0]
            except:
                traceback.print_exc()
            try:
                item['duoban_score'] = response.xpath('//*[@property="v:average"]/text()').extract()[0]
            except:
                traceback.print_exc()
            try:
                item['duoban_votes'] = response.xpath('//*[@property="v:votes"]/text()').extract()[0]
            except:
                traceback.print_exc()
            try:
                item['tags'] = response.xpath('//div[@class="tags-body"]/a/text()').extract()
            except:
                traceback.print_exc()
            try:
                item['abstract'] = response.xpath('//*[@property="v:summary"]/text()').extract()[0].replace('\"','').strip()
            except:
                traceback.print_exc()
            
            yield item
        except:
            traceback.print_exc()
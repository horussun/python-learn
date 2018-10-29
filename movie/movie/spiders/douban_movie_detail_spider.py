# -*- coding: utf-8 -*-
# @Time     : 2018/9/7 17:04
# @Author   : SWZ


from scrapy import Request
from scrapy.spiders import Spider
from movie.items import DoubanMovieItem
#import json
#from scrapy.selector import Selector
#import random
#from movie.proxy.pool_proxy import proxypool

#scrapy crawl douban_movie_detail -o douban-de.csv
class DoubanMovieDetailSpider(Spider):
    name = 'douban_movie_detail'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        start_url = 'https://movie.douban.com/subject/27072795/'
        yield Request(start_url, headers=self.headers, meta={'start_url':start_url})

    def parse(self, response):
        item = DoubanMovieItem()
        item['movie_url'] = response.meta['start_url']
        item['movie_id'] = response.meta['start_url'][33:-1]
        item['movie_name'] = response.xpath('//span[@property="v:itemreviewed"]/text()').extract()[0]
        item['director'] = response.xpath('//span/a[@rel="v:directedBy"]/text()').extract()[0]
        item['scriptwriter'] = response.xpath('//div[@id="info"]/span[2]/span[@class="attrs"]/a/text()').extract()
        item['actor'] = response.xpath('//*[@rel="v:starring"]/text()').extract()
        item['genres'] = response.xpath('//*[@property="v:genre"]/text()').extract()
        item['year'] = response.xpath('//*[@property="v:initialReleaseDate"]/text()').extract()[0][0:4]
        item['release_date'] = response.xpath('//*[@property="v:initialReleaseDate"]/text()').extract()
        item['area'] = response.xpath('//*[@id="info"]').re('制片国家/地区:</span>\s(.*)<br>')
        try:
            #item['runtime'] = response.xpath('//*[@property="v:runtime"]/text()').re(r'(\d+)')[0]
            item['runtime'] = response.xpath('//*[@property="v:runtime"]/text()').re(r'(^([^\(]*)\(.*$)')[0]
        except Exception as e:
            print(e)
        #item['imdb_url'] = 'http://www.imdb.com/title/'+response.xpath('//*[@rel="nofollow"]/text()').extract()[0]
        try:
            item['duoban_score'] = response.xpath('//*[@property="v:average"]/text()').extract()[0]
        except Exception as e:
            print(e)
        try:
            item['duoban_votes'] = response.xpath('//*[@property="v:votes"]/text()').extract()[0]
        except Exception as e:
            print(e)
        try:
            item['tags'] = response.xpath('//div[@class="tags-body"]/a/text()').extract()
        except Exception as e:
            print(e)
        item['abstract'] = response.xpath('//*[@property="v:summary"]/text()').extract()[0].replace('\"','').strip()
        
        yield item
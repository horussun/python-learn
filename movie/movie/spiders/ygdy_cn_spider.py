# -*- coding: utf-8 -*-
# @Time     : 2018/9/7 17:04
# @Author   : SWZ


from scrapy import Request
from scrapy.spiders import Spider
from movie.items import DoubanMovieItem
import json
import sys

#scrapy crawl ygdy_movie_cn -o ygdy-cn.csv
class DoubanMovieCNSpider(Spider):
    name = 'ygdy_movie_cn'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'http://www.ygdy8.com/html/gndy/china/list_4_1.html'
        yield Request(url, headers=self.headers)

    def parse(self, response):
        item = DoubanMovieItem()
        print('*'*30)
        movies = response.xpath('//div[@class="co_content8"]/ul/td/table')
        print(movies[2].xpath("//div[@class='co_content8']/ul/td/table/tr/td/b/a/text()").extract()[1])
        #print(movies)
        #for movie in movies:
        #    item['movie_url'] = movie.xpath("//div[@class='co_content8']/ul/td/table/tr/td/b/a/@href").extract()[1]
        #    yield item
            
    def parse_detail(self, response):
        try:
            item = DoubanMovieItem()
            item['movie_url'] = response.meta['start_url']
            item['movie_id'] = response.meta['start_url'][33:-1]
            item['movie_name'] = response.xpath('//span[@property="v:itemreviewed"]/text()').extract()[0]
            item['director'] = response.xpath('//span/a[@rel="v:directedBy"]/text()').extract()[0]
            item['writer'] = response.xpath('//div[@id="info"]/span[2]/span[@class="attrs"]/a/text()').extract()
            item['actor'] = response.xpath('//*[@rel="v:starring"]/text()').extract()
            item['genres'] = response.xpath('//*[@property="v:genre"]/text()').extract()
            item['year'] = response.xpath('//*[@property="v:initialReleaseDate"]/text()').extract()[0][0:4]
            item['ymd'] = response.xpath('//*[@property="v:initialReleaseDate"]/text()').extract()[0][0:10]
            item['area'] = response.xpath('//*[@property="v:initialReleaseDate"]/text()').extract()[0][11:15]
            try:
                #item['runtime'] = response.xpath('//*[@property="v:runtime"]/text()').re(r'(\d+)分钟')[0]
                item['runtime'] = response.xpath('//*[@property="v:runtime"]/text()').extract()[0][0:-2]
            except Exception as e:
                print(e)
            #item['imdb_url'] = 'http://www.imdb.com/title/'+response.xpath('//*[@rel="nofollow"]/text()').extract()[0]
            try:
                item['score'] = response.xpath('//*[@property="v:average"]/text()').extract()[0]
            except Exception as e:
                print(e)
            try:
                item['votes'] = response.xpath('//*[@property="v:votes"]/text()').extract()[0]
            except Exception as e:
                print(e)
            try:
                item['tags'] = response.xpath('//div[@class="tags-body"]/a/text()').extract()
            except Exception as e:
                print(e)
            #item['abstract'] = response.xpath('//*[@property="v:summary"]/text()').extract()[0]
            
            yield item
        except Exception as e:
            print(e)
'''
Created on 2018年9月5日

@author: swz
'''
from scrapy.spiders import Spider

#scrapy crawl test_spider
class BlogSpider(Spider):
    name = 'test_spider'
    start_urls = ['http://woodenrobot.me']

    def parse(self, response):
        titles = response.xpath('//a[@class="post-title-link"]/text()').extract()
        
        for title in titles:
            print(title.strip())
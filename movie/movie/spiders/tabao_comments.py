'''
Created on 2018年9月27日

@author: swz
'''
from scrapy import Request
from scrapy.spiders import Spider
import string
import random
import json
import time
from movie.items import TaobaoCommentItem

#scrapy crawl taobao_commentes -o wbsys-comments.csv
class TaobaoCommentsSpider(Spider):
    name = 'taobao_commentes'
    #allowed_domains = ["detail.tmall.com"]
    url = "https://rate.tmall.com/list_detail_rate.htm?itemId=575397228277&spuId=1036717683&sellerId=430490406&order=3&currentPage={}&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%23E1hvovvbvnQvUpCkvvvvvjiPPsLUtjr8R2SW0jivPmPWQj1hRsS90j3URFcvzj1WRLyCvvpvvhCv3QhvCvmvphm5vpvhvvCCBUyCvvOCvhEC0RoivpvUvvCCETLQwEmtvpvIvvCvxQvvvUvvvhc4vvvva9vvBJZvvUHmvvCHtpvv94hvvhc4vvmCIpyCvhACERj3j47J%2Bu6XjobysEk4jX31BW2vHFKzrmphQRA1%2BbeAOHjWT2eARdIAcUmxdBAK5kx%2Fgj7xhL%2BtExVtkC465iDsoYmQRqJ6WeCpvphvC9vhphvvvvGCvvLMMQvvRphvCvvvphmCvpvZz2QedlbNznswnEHfYqzw9YAv7Ih%3D&needFold=0&_ksTS=1538290197177_4431&callback=jsonp4432"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        #for i in range(1,4):
        #to_url = self.url.format(1)
        yield Request(self.url, headers=self.headers)

    def parse(self, response):
        item = TaobaoCommentItem()
        comments = json.loads(response.body_as_unicode())
        comments = comments['rateList']
        for comment in comments:
            print(comment['rateContent'])
            #yield item

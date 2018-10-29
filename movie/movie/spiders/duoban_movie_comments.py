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
from selenium import webdriver
from movie.items import DuobanMovieCommentItem

#scrapy crawl douban_movie_commentes -o wbsys-comments.csv
class DoubanMovieCommentsSpider(Spider):
    name = 'douban_movie_commentes'
    allowed_domains = ["movie.douban.com"]
    start_urls = [
        "https://movie.douban.com/subject/26752088/comments?status=P",
        "https://movie.douban.com/subject/26752088/comments?status=F"
    ]

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "movie.douban.com",
        "Referer": "https://movie.douban.com/",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
    }

    '''
    cookies = {"ll": "118159", "bid": "pwfVXwRezic", "__yadk_uid": "sSRJaB2vjBBkTfN6m7qK88sCxq9yiD5y",
        "_vwo_uuid_v2": "FFAFD09BFF20B3EB48CC2E5732174951|ced283bb85c6ec322963dd59f5188cfb", "ap": "1",
        "_pk_ref.100001.4cf6": "%5B%22%22%2C%22%22%2C1503235681%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D",
        "_pk_id.100001.4cf6": "5df75a257f8998e5.1498916085.6.1503235681.1503231672.", "_pk_ses.100001.4cf6": "*",
        "__utmt_douban": "1", "__utma": "30149280.1451420405.1498916085.1503233585.1503235681.11",
        "__utmb": "30149280.1.10.1503235681", "__utmc": "30149280",
        "__utma": "223695111.1318916198.1498916085.1503230049.1503235681.6",
        "__utmb": "223695111.0.10.1503235681", "__utmc": "223695111"}
    '''

    cookies = ""
    driver = webdriver.Chrome(
        executable_path="/Users/swz/workspace/python/movie/chromedriver")

    def web_login(self):
        # 模拟登陆豆瓣
        self.driver.get("https://accounts.douban.com/login?source=movie")
        # 用户名 密码
        elem_user = self.driver.find_element_by_name("form_email")
        elem_user.send_keys("**************")
        time.sleep(1.5)
        elem_pwd = self.driver.find_element_by_name("form_password")
        elem_pwd.send_keys("********")
        time.sleep(1.5)
        self.driver.find_element_by_id("remember").click()
        time.sleep(4)
        self.driver.find_element_by_name("login").click()
        time.sleep(3)
        self.driver.get(
            "https://movie.douban.com/subject/27135550/comments?status=P")
        time.sleep(3)
        cookiestr = ""
        for item in self.driver.get_cookies():
            name = item["name"]
            value = item["value"]
            cookiestr = cookiestr + '"' + \
                name.replace('"', '') + '":"' + value.replace('"', '') + '", '
        cookiestr = "{" + cookiestr[0:len(cookiestr) - 2] + "}"
        print(cookiestr)
        self.cookies = json.loads(cookiestr)

    def start_requests(self):
        self.web_login()
        print(self.cookies)
        for url in self.start_urls:
            self.cookies["bid"] = "".join(random.sample(
                string.ascii_letters + string.digits, 11))
            yield Request(url, headers=self.headers, cookies=self.cookies)

    def parse(self, response):
        item = DuobanMovieCommentItem()
        comments = response.xpath('//div[@class="comment-item"]')
        for comment in comments:
            item['user_name'] = comment.xpath(
                './/span[@class="comment-info"]/a/text()').extract_first()
            item['comment_time'] = comment.xpath(
                './/span[@class="comment-time "]/@title').extract_first()
            is_view = comment.xpath(
                './/span[@class="comment-info"]/span/text()').extract_first()
            infos = comment.xpath('.//span[@class="comment-info"]/span')
            item['is_view'] = is_view
            if is_view == u'看过':
                if len(infos) == 2:
                    item['score'] = u'无评分'
                else:
                    item['score'] = comment.xpath(
                        './/span[@class="comment-info"]/span[2]/@title').extract_first()
            else:
                item['score'] = u'无评分'
            item['agree_num'] = comment.xpath(
                './/span[@class="votes"]/text()').extract_first()
            item['comment'] = comment.xpath(
                './/div[@class="comment"]/p/span[@class="short"]/text()').extract_first()
            yield item

        next_page_url = response.xpath(
            '//a[@class="next"]/@href').extract_first()
        if next_page_url is not None:
            self.cookies["bid"] = "".join(random.sample(
                string.ascii_letters + string.digits, 11))
            yield Request("https://movie.douban.com/subject/26752088/comments" + next_page_url, 
                          callback=self.parse, headers=self.headers, cookies=self.cookies)

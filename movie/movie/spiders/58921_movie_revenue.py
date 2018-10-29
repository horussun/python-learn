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
from movie.items import MovieRevenueItem

#scrapy crawl movie_revenue -o movie_revenue.csv
class MovieRevenueSpider(Spider):
    name = 'movie_revenue'
    allowed_domains = ["58921.com"]
    start_urls = [
        "http://58921.com/alltime?page=0"
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
        self.driver.get("http://58921.com/user/login")
        # 用户名 密码
        elem_user = self.driver.find_element_by_name("mail")
        elem_user.send_keys("*********")
        time.sleep(1.5)
        elem_pwd = self.driver.find_element_by_name("pass")
        elem_pwd.send_keys("******")
        time.sleep(1.5)
        self.driver.find_element_by_id("user_login_form_type_his_1").click()
        time.sleep(2)
        self.driver.find_element_by_name("submit").click()
        time.sleep(2)
        self.driver.get("http://58921.com/alltime?page=0")
        time.sleep(2)
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
        url = "http://58921.com/alltime?page={}"
        for i in range(1):
            to_url = url.format(i)
            self.cookies["bid"] = "".join(random.sample(string.ascii_letters + string.digits, 11))
            yield Request(to_url, headers=self.headers, cookies=self.cookies)

    def parse(self, response):
        item = MovieRevenueItem()
        comments = response.xpath('//table[@class="center_table movie_box_office_stats_table table table-bordered table-condensed"]/tbody')
        for comment in comments:
            item['movie_name'] = comment.xpath('.//td/a/text()').extract_first()
            item['revenue'] = comment.xpath('.//td/img/text()').extract_first()
            item['year'] = comment.xpath('.//td/text()').extract_first()
            
            yield item

#由于douban对于爬虫的限制，一是慢怕，二是用代理，免费代理、效果不佳
#一慢爬，代码/move/spiders/douban_spider.py，修改url里面的参数tag、countory可爬所需内容
#在settings文件里面设置DOWNLOAD_DELAY = 1，DOWNLOADER_MIDDLEWARES = {'movie.middlewares.RandomUserAgent': 1,}
运行：
scrapy crawl douban_movie -o douban-cn.csv


#二是代理，使用免费的代理效果不佳，
#在settings文件里面设置DOWNLOAD_DELAY = 0.25，DOWNLOADER_MIDDLEWARES = {#'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,'movie.proxy.randomproxy.RandomProxy': 100,'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,}
运行：
scrapy crawl douban_movie -o douban-cn.csv

#代理使用代码/movie/proxy/fetch_douban_movies.py，效果不佳，后续需要代码增加在使用代理时判定代理是否可用
用之前用fetch_proxy.py取得代理host.txt
用python运行fetch_douban_movies.py
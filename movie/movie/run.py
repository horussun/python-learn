# -*- coding: utf-8 -*-

from scrapy import cmdline


name = 'douban_movie_top250'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())

#scrapy crawl somespider -s JOBDIR=crawls/somespider-1 持久化

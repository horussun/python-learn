# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from jinja2 import runtime


class MovieItem(scrapy.Item):
    movie_imdb_link = scrapy.Field()
    imdb_score = scrapy.Field()
    movie_title = scrapy.Field()
    title_year = scrapy.Field()
    num_voted_users = scrapy.Field()
    genres = scrapy.Field()
    budget = scrapy.Field()
    color = scrapy.Field()
    gross = scrapy.Field()
    duration = scrapy.Field()
    country = scrapy.Field()
    language = scrapy.Field()
    plot_keywords = scrapy.Field()
    storyline = scrapy.Field()
    aspect_ratio = scrapy.Field()
    content_rating = scrapy.Field()
    num_user_for_reviews = scrapy.Field()
    num_critic_for_reviews = scrapy.Field()
    cast_info = scrapy.Field()
    director_info = scrapy.Field()
    num_facebook_like = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()

    
class MovieBudgetItem(scrapy.Item):
    num_rows = scrapy.Field()
    release_date = scrapy.Field()
    movie_link = scrapy.Field()
    movie_name = scrapy.Field()
    production_budget = scrapy.Field()
    domestic_gross = scrapy.Field()
    worldwide_gross = scrapy.Field() 


class ImdbUrlItem(scrapy.Item):
    movie_name = scrapy.Field()
    movie_imdb_link = scrapy.Field()


class PosterImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()


class DoubanMovieItem(scrapy.Item):
    movie_id = scrapy.Field()
    # 电影名称
    movie_name = scrapy.Field()
    scriptwriter = scrapy.Field()
    director = scrapy.Field()
    actor = scrapy.Field()
    movie_url = scrapy.Field()
    imdb_url = scrapy.Field()
    runtime = scrapy.Field()
    genres = scrapy.Field()
    year = scrapy.Field()
    release_date = scrapy.Field()
    area = scrapy.Field()
    #ranking = scrapy.Field()
    duoban_score = scrapy.Field()
    duoban_votes = scrapy.Field()
    duoban_comments = scrapy.Field()
    tags = scrapy.Field()
    abstract = scrapy.Field()
    budget = scrapy.Field()
    revenue = scrapy.Field()
    
class DuobanMovieCommentItem(scrapy.Item):
    user_name = scrapy.Field()
    comment_time = scrapy.Field()
    score = scrapy.Field()
    agree_num = scrapy.Field()
    comment = scrapy.Field()
    is_view = scrapy.Field()
    
class TaobaoCommentItem(scrapy.Item):
    comment = scrapy.Field()
    rate_date = scrapy.Field()
    
class MovieRevenueItem(scrapy.Item):
    movie_name = scrapy.Field()
    revenue = scrapy.Field()
    year = scrapy.Field()
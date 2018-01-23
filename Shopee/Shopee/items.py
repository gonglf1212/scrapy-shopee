# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class GoodsItem(scrapy.Item):
    itemid = scrapy.Field()
    shopid = scrapy.Field()
    price= scrapy.Field()
    price_max = scrapy.Field()
    liked_count = scrapy.Field()
    price_min = scrapy.Field()
    rating_star = scrapy.Field()
    rating_all = scrapy.Field()
    rating_count = scrapy.Field()
    hashtag_list = scrapy.Field()
    catid = scrapy.Field()
    categories = scrapy.Field()
    ctime = scrapy.Field()
    sold = scrapy.Field()
    currency = scrapy.Field()
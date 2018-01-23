# -*- coding: utf-8 -*-
import scrapy
import json
from Shopee.items import GoodsItem


class ShopeeSpider(scrapy.Spider):
    name = 'shopee'

    def __init__(self):
        self.allowed_domains = ['shopee.tw']
        self.category_list_url = "https://mall.shopee.tw/api/v2/category_list/get"
        self.subcategory_list_url = "https://mall.shopee.tw/api/v2/subcategory_list/get?catid="
        self.search_items = "https://mall.shopee.tw/api/v2/search_items?by=pop&limit=50&order=desc&page_type=search"
        self.get_url = "https://mall.shopee.tw/api/v2/item/get?"
        self.start_urls = [self.category_list_url]

    def parse(self, response):
        data_list = json.loads(response.body)['data']['category_list']
        for data in data_list:
            url = self.subcategory_list_url + str(data['catid'])
            yield scrapy.Request(url, callback=self.parse_subcategory)

    def parse_subcategory(self, response):
        data_list = json.loads(response.body)['data']['category_list']
        for data in data_list:
            url = self.search_items + "&newest=0&match_id={}".format(data['catid'])
            yield scrapy.Request(url, callback=self.parse_search, meta={'catid': data['catid'], 'newest':0})

    def parse_search(self, response):
        cat_id = response.meta['catid']
        newest = response.meta['newest']
        data_list = json.loads(response.body)['items']
        if len(data_list) == 0:
            return
        for data in data_list:
            url = self.get_url + "itemid={}&shopid={}".format(data['itemid'], data['shopid'])
            yield scrapy.Request(url, callback=self.parse_items, meta={'itemid': data['itemid']})
        url = self.search_items + "&newest={}&match_id={}".format(newest+50, cat_id)
        yield scrapy.Request(url, callback=self.parse_search, meta={'catid': cat_id, 'newest':newest+50})

    def parse_items(self, response):
        data_list = json.loads(response.body, encoding="utf-8")['item']
        if len(data_list) == 0:
            return
        item = GoodsItem()
        item['itemid'] = data_list['itemid']
        item['shopid'] = data_list['shopid']
        item['price'] = data_list['price']
        if data_list['price_max'] == -1:
            item['price_max'] = 0
        else:
            item['price_max'] = data_list['price_max']
        if data_list['price_min'] == -1:
            item['price_min'] = 0
        else:
            item['price_min'] = data_list['price_min']
        item['liked_count'] = data_list['liked_count']
        item['rating_star'] = data_list['item_rating']['rating_star']
        item['rating_all'] = data_list['item_rating']['rating_count'][0]
        item['rating_count'] = ',' .join(map(str,data_list['item_rating']['rating_count']))
        item['hashtag_list'] = ','.join(data_list['hashtag_list'])
        item['catid'] = data_list['catid']
        categories = []
        for catId in data_list['categories']:
            categories.append(catId['catid'])
        item['categories'] = ','.join(map(str,categories))
        item['ctime'] = data_list['ctime']
        solds = 0
        for sold in data_list['models']:
            solds += sold['sold']
        item['sold'] = solds
        item['currency'] = data_list['currency']
        yield item



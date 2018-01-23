# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from Shopee.Mysql import MySql
from Shopee.MyRedis import MyRedis


class ShopeePipeline(object):

    myRedis = MyRedis()
    mysql = MySql()

    def process_item(self, item, spider):
        try:
            self.mysql.insert_db(item)
            self.myRedis.insert_redis(item)
        except Exception as e:
            print("异常--", e)
        return item



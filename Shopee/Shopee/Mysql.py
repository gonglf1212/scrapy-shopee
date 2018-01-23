# -*- coding: utf-8 -*-
import pymysql
from Shopee import settings


class MySql(object):

    db = pymysql.connect("localhost", settings.DB_USERNAME, settings.DB_PASSWORD, settings.DB_NAME, charset='utf8')
    cursor = db.cursor()

    def __init__(self):
        pass

    def insert_db(self, item):
        sql = """INSERT INTO product(itemid, shopid, price, price_max, liked_count, price_min, rating_star,
 rating_all, rating_count, hashtag_list, catid, categories, ctime, sold, currency) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        values = (item['itemid'], item['shopid'], item['price'], item['price_max'], item['liked_count'], item['price_min'], item['rating_star'], item['rating_all'], item['rating_count'], item['hashtag_list'], item['catid'], item['categories'], item['ctime'], item['sold'], item['currency'])
        try:
            self.cursor.execute(sql, values)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise

    def select_item_db(self):
        sql = "SELECT itemid FROM product"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def select_num_db(self):
        sql = "SELECT COUNT(id) FROM product"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result

    def __del__(self):
        self.db.close()
        pass
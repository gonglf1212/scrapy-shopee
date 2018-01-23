# -*- coding: utf-8 -*-
import redis
from Shopee.Mysql import MySql


class MyRedis:
    redis_db = redis.Redis(host='127.0.0.1', port=6379, db=0)
    redis_data_dict = "itemid"
    mySql = MySql()

    def __init__(self):
        dbnum = self.mySql.select_num_db()[0]
        renum = self.redis_db.scard('itemid')
        if dbnum != renum:
            self.redis_db.flushdb()
            if self.redis_db.hlen(self.redis_data_dict) == 0:  #
                datas = self.mySql.select_item_db()
                for itemId in datas:
                    self.redis_db.sadd(self.redis_data_dict, itemId[0])

    def is_exit(self, itemId):
        if self.redis_db.sismember(self.redis_data_dict, itemId):
            print(itemId, ':---exists')
            return False
        else:
            return True

    def insert_redis(self, item_id):
        self.redis_db.sadd(self.redis_data_dict, item_id)

    def __del__(self):
        pass

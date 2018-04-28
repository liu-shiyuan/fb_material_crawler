# -*- coding:utf-8 -*-
import redis
from config import *
from logger_provider import *
import time


__redis_host__ = config.get('redis.host')
__redis__port__ = config.get('redis.port')
__redis__db__ = config.get('redis.database')
__redis__key__ = config.get('redis.crawl.url.key')


def __get_redis_conn__():
    # connection_pool = redis.ConnectionPool(host=__redis__port__, port=__redis__port__, db=__redis__db__)
    # return redis.Redis(connection_pool=connection_pool)
    return redis.Redis(host=__redis_host__, port=__redis__port__, db=__redis__db__)


r = __get_redis_conn__()


def consume_url_queue():
    return r.lpop(__redis__key__)


def has_next_crawl_url():
    global r
    time.sleep(0.5)
    if r:
        if r.ping():
            if r.keys(__redis__key__):
                return True
            else:
                return False
    get_logger().debug('redis connection expired, get new connection.')
    try:
        r = __get_redis_conn__()
    except Exception as e:
        get_logger().error('error occurred when get redis connection')
        if e and e.msg:
            get_logger().error(e.msg)
        return False


if __name__ == '__main__':
    print(consume_url_queue())

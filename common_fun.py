# -*- coding:utf-8 -*-
from urllib import parse
from selenium.common.exceptions import NoSuchElementException
from crawl_exception.violate_censorship_exception import ViolateCensorshipException
from chrome_driver import *
from logger_provider import *
#from phantomjs_driver import *
import urllib
from urllib.request import ProxyHandler, build_opener
import re


def get_app_bag(store_url):
    if not store_url:
        return ''
    if store_url.find('play.google.com') < 0 and store_url.find('itunes.apple.com') < 0:
        return ''

    store_url = remove_fb_domain(store_url)
    store_url = parse.unquote_plus(store_url)
    i = store_url.find('id=')
    if i == -1:
        i = store_url.find('id')
        store_url = store_url[i + 2:]
        j = store_url.find('?')
        if j != -1:
            store_url = store_url[0:j]
    else:
        store_url = store_url[i + 3:]
        j = store_url.find('&')
        if j != -1:
            store_url = store_url[0:j]
    return store_url


def get_pic_name(url):
    i = url.rfind('/')
    j = url.rfind('?')
    return url[i + 1:j]


def remove_fb_domain(url):
    i = url.rfind('https')
    return url[i:]


def get_element_by_xpaths(driver, xpaths):
    xpaths = xpaths.split(',')
    for xpath in xpaths:
        try:
            element = driver.find_element_by_xpath(xpath.strip())
            return element
        except NoSuchElementException as e:
            pass
    raise NoSuchElementException(xpaths)


def get_fb_page(url):
    # 'https://www.facebook.com/danubeproperties/posts/2052528158369370' => danubeproperties
    blocks = url.split('/')
    if len(blocks) >= 4:
        get_logger().debug('get page from: ' + url + ' got :' + blocks[3])
        return blocks[3]
    return 'default'


def get_fb_post_id(url):
    blocks = url.split('/')
    if len(blocks) >= 6:
        if blocks[len(blocks) - 1]:
            get_logger().debug('get page from: ' + url + ' got :' + blocks[len(blocks) - 1])
            return blocks[len(blocks) - 1]
        elif blocks[len(blocks) - 2]:
            get_logger().debug('get page from: ' + url + ' got :' + blocks[len(blocks) - 2])
            return blocks[len(blocks) - 2]
    return ''


def valid_store_url(url):
    if not url:
        return False
    if 'play.google.com' in url:
        return True
    if 'itunes.apple.com' in url:
        return True
    return False


def get_default_driver(locale=None):
    return get_driver(locale=locale)


def record_url(url, locale=None):
    if locale:
        get_record_logger().info(locale + ': ' + url)
    else:
        get_record_logger().info(url)


def set_urllib_proxy():
    if config.get('proxy.need') == 1:
        proxy = config.get('proxy.host') + ':' + str(config.get('proxy.port'))
        proxy_handler = ProxyHandler({
            'http': 'http://' + proxy,
            'https': 'https://' + proxy
        })
        opener = build_opener(proxy_handler)
        urllib.request.install_opener(opener)


censorship = ['dafa', 'falun', 'lihongzhi', '法轮', '法輪']


def validate_url(url):
    global censorship
    for bad_word in censorship:
        if re.search(bad_word, url, re.IGNORECASE):
            reason = 'violate censorship URL: ' + url
            raise ViolateCensorshipException(reason=reason)



if __name__ == '__main__':
    _url = 'https://scontent-hkg3-2.xx.fbcdn.net/v/t45.1600-4/cp0/q90/c1.0.1199.627/s480x480/12061660_6033662864979_886736569_n.png.jpg?_nc_cat=0&efg=eyJxZV9ncm91cHMiOlsibm9fc2FmZV9pbWFnZV9mb3JfYWRzX2ltYWdlIl19&oh=e45dae3671e6a3d0df78371c16c6698a&oe=5B2D25BE'
    #print(get_pic_name(_url))
    x = 'https://www.facebook.com/danubeproperties/posts/2052528158369370'
    print(get_fb_post_id(x))

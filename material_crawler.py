# -*- coding:utf-8 -*-
from crawler_url_provider import *
from config import *
from logger_provider import *
from common_fun import *
from urllib import parse
from download_video import VideoDownloader
from download_carousel import CarouselDownloader
from download_pic import PicDownloader
from selenium.common.exceptions import WebDriverException
from crawl_exception.crawling_exception import NotBannerException


BANNER_TIMEOUT = config.get('crawl.banner.timeout')
CAROUSEL_TIMEOUT = config.get('crawl.carousel.timeout')
VIDEO_TIMEOUT = config.get('crawl.video.timeout')


driver = None
while True:
    if has_next_crawl_url():
        try:
            url = consume_url_queue()
            try:
                url = url.decode('utf-8')
            except UnicodeDecodeError as e:
                get_logger().error('error occurred when decode url: ' + str(url) + ', and reason: ' + e.reason)
                continue
            url = parse.unquote(url)

            validate_url(url)

            locale = None

            if '|' in url:
                url_with_locale = url.split('|')
                url = url_with_locale[1]
                locale = url_with_locale[0]

            record_url(url, locale)
            get_logger().info('start crawling for: ' + url)
            fb_page_name = get_fb_page(url)
            if not fb_page_name:
                fb_page_name = 'defaultpage'
            fb_post_id = get_fb_post_id(url)
            driver = get_default_driver(locale)

            if url.find('/videos/') > -1 or url.find('/video/') > -1:
                VideoDownloader(driver=driver, page=fb_page_name, post_id=fb_post_id
                                , locale=locale, timeout_seconds=VIDEO_TIMEOUT).download(url)
            else:
                driver.get(url)
                try:
                    # _79n img sp_Fkzo23bT_dJ_2x sx_6a6934
                    # _4fby _79k _79m _4-u8
                    is_carousel = driver.find_element_by_class_name('_4fby')
                    CarouselDownloader(driver=driver, page=fb_page_name, post_id=fb_post_id
                                       , locale=locale, timeout_seconds=CAROUSEL_TIMEOUT).download()
                except:
                    try:
                        PicDownloader(driver=driver, page=fb_page_name, post_id=fb_post_id
                                      , locale=locale, timeout_seconds=BANNER_TIMEOUT).download()
                    except NotBannerException as nbe:
                        known_app_bag_name = None
                        if nbe.reason:
                            known_app_bag_name = nbe.reason
                        VideoDownloader(driver=driver, page=fb_page_name, post_id=fb_post_id
                                        , locale=locale, timeout_seconds=VIDEO_TIMEOUT, app_bag_name=known_app_bag_name).download(url)
            get_logger().info('done with: ' + url)
        except Exception as e:
            if e:
                get_logger().debug('error occurred while crawling:')
                if hasattr(e, 'reason'):
                    get_logger().error('Exception: ' + str(e.reason))
                else:
                    get_logger().error('Exception: ' + str(e))
            try:
                if driver:
                    driver.quit()
            except WebDriverException as e:
                get_logger().error('Exception occurred when close driver: ' + e.msg)
    else:
        get_logger().info('No more material to crawl for now.')
        time.sleep(60)


if __name__ == '__main__':
    pass


# -*- coding:utf-8 -*-
from config import *
from chrome_driver import *
from common_fun import *
import urllib.request
from selenium.common.exceptions import NoSuchElementException
from time_limit import *
import platform
from crawl_exception.crawling_exception import NotBannerException
from screenshot_capture import *


class PicDownloader:
    def __init__(self, driver=None, page='', post_id='', locale=None, timeout_seconds=None):
        if driver:
            self._driver = driver
        else:
            self._driver = get_driver()
        self._timeout_seconds = timeout_seconds
        self._page = page
        self._post_id = post_id
        self._locale = locale

    def __download__(self, pic_url=None):
        if pic_url:
            self._driver.get(pic_url)
        # try:
        #     call_to_action = self._driver.find_element_by_xpath(config.get('call.to.action.btn.xpath'))
        # except NoSuchElementException as e:
        #     self._driver.find_element_by_xpath(config.get('close.expand.ad.btn.xpath')).click()
        #     call_to_action = self._driver.find_element_by_xpath(config.get('call.to.action.btn.xpath2'))
        try:
            self._driver.find_element_by_xpath(config.get('close.expand.ad.btn.xpath')).click()
        except:
            pass

        try:
            self._driver.execute_script('document.getElementsByClassName("_3ob9")[0].style.display="None"')
        except:
            pass

        store_url = None
        call_to_actions = self._driver.find_elements_by_tag_name('a')
        if call_to_actions:
            for call_to_action in call_to_actions:
                if call_to_action.get_attribute('role') == 'button':
                    if valid_store_url(call_to_action.get_property('href')):
                        store_url = call_to_action.get_property('href')
                        break
        app_bag = get_app_bag(store_url)
        imgs = self._driver.find_elements_by_class_name(config.get('pic.img.class.name'))
        # scaledImageFitHeight
        try:
            strange_imgs = self._driver.find_elements_by_class_name('scaledImageFitHeight')
            if strange_imgs:
                imgs = imgs + strange_imgs
        except:
            pass

        set_urllib_proxy()
        is_video = True

        base_store_url = config.get('base.pic.store.dir')
        if self._locale:
            base_store_url = os.path.join(base_store_url, self._locale)
        store_path = os.path.join(base_store_url, self._page)
        store_path = os.path.join(store_path, app_bag)
        store_path = os.path.join(store_path, 'banner')
        store_path = os.path.join(store_path, self._post_id)

        for img in imgs:
            if img.get_attribute('itemprop'):
                continue
            src = img.get_property('src')
            if not os.path.exists(store_path):
                os.makedirs(store_path)
            final_file_name = os.path.join(store_path, get_pic_name(src))
            get_logger().debug('downloading banner: ' + src)
            urllib.request.urlretrieve(src, final_file_name)
            is_video = False
            get_logger().debug('download banner done: ' + src)
            #break
        if is_video:
            raise NotBannerException(app_bag)
        take_banner_screenshot(self._driver, store_path)
        self._driver.close()

    def download(self, pic_url=None):
        if self._timeout_seconds and 'linux' == platform.system().lower():
            try:
                with time_limit(self._timeout_seconds):
                    self.__download__(pic_url)
            except TimeoutException:
                self._driver.close()
                print("time out")
        else:
            self.__download__(pic_url)


if __name__ == '__main__':
    x = 'https://www.facebook.com/houseoffungames/posts/1831417040236479'
    y = 'https://www.facebook.com/Relaapp/posts/773251762867414'
    z = 'https://www.facebook.com/shigen.ryu/posts/1343481579086637'
    PicDownloader(page='shigen.ryu', post_id='1343481579086637').download(z)
    #PicDownloader(page='houseoffungames', post_id='1831417040236479').download(x)

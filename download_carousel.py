# -*- coding:utf-8 -*-
from config import *
from chrome_driver import *
from selenium.common.exceptions import NoSuchElementException
import urllib.request
from common_fun import *
import platform
from time_limit import *
from logger_provider import *
from screenshot_capture import *


class CarouselDownloader:
    def __init__(self, driver=None, page='', post_id='', locale=None, timeout_seconds=None):
        if driver:
            self._driver = driver
        else:
            self._driver = get_driver()
        self._timeout_seconds = timeout_seconds
        self._page = page
        self._post_id = post_id
        self._app_bag_name = None
        self._locale = locale

    def __download__(self, carousel_url=None):
        if carousel_url:
            self._driver.get(carousel_url)
        try:
            self._driver.find_element_by_xpath(config.get('close.expand.ad.btn.xpath')).click()
        except:
            get_logger().debug("no expand ad")

        try:
            self._driver.execute_script('document.getElementsByClassName("_3ob9")[0].style.display="None"')
        except:
            pass

        carousel_imgs = self._driver.find_elements_by_class_name('_kvn')
        buttons = self._driver.find_elements_by_tag_name('button')
        for button in buttons:
            if valid_store_url(button.get_attribute('href')):
                button_href = button.get_attribute('href')
            #if button_href:
                self._app_bag_name = get_app_bag(button_href)

        base_store_url = config.get('base.carousel.store.dir')
        if self._locale:
            base_store_url = os.path.join(base_store_url, self._locale)
        store_path = os.path.join(base_store_url, self._page)
        if self._app_bag_name:
            store_path = os.path.join(store_path, self._app_bag_name)
        store_path = os.path.join(store_path, 'carousel')
        if self._post_id:
            store_path = os.path.join(store_path, self._post_id)
        if not os.path.exists(store_path):
            os.makedirs(store_path)

        set_urllib_proxy()

        for img in carousel_imgs:
            src = img.get_property('src')
            final_file_name = os.path.join(store_path, get_pic_name(src))
            get_logger().debug('downloading carousel: ' + src)
            urllib.request.urlretrieve(src, final_file_name)
            get_logger().info('download carousel done: ' + src)

        take_carousel_screenshot(self._driver, store_path)
        self._driver.close()

    def download(self, carousel_url=None):
        if self._timeout_seconds and 'linux' == platform.system().lower():
            try:
                with time_limit(self._timeout_seconds):
                    self.__download__(carousel_url)
            except TimeoutException:
                self._driver.close()
                print("time out")
        else:
            self.__download__(carousel_url)


if __name__ == '__main__':
    x = 'https://www.facebook.com/danubeproperties/posts/2052528158369370'
    CarouselDownloader(page='danubeproperties', post_id='2052528158369370').download(x)
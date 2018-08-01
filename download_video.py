# -*- coding:utf-8 -*-
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import os
from config import *
from chrome_driver import *
import platform
from time_limit import *
import urllib.request
from common_fun import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class VideoDownloader:
    def __init__(self, driver=None, page='', post_id='', app_bag_name=None, timeout_seconds=None, locale=None):
        # init a driver first
        if driver:
            self._driver = driver
        else:
            self._driver = get_driver()
        # set time out
        self._timeout_seconds = timeout_seconds
        self._page = page
        self._post_id = post_id
        self._app_bag_name = app_bag_name
        self._locale = locale

    def __download__(self, video_url):
        set_urllib_proxy()
        crawl_video_agent = config.get('crawl.video.agent')
        self._driver.get(crawl_video_agent)
        search_text = self._driver.find_element_by_id('sf_url')
        search_text.send_keys(video_url)
        #btn = self._driver.find_element_by_name('sf_submit')
        get_logger().debug('wait for page render')
        btn = WebDriverWait(self._driver, 15).until(EC.element_to_be_clickable((By.ID, "sf_submit")))
        get_logger().debug('button is clickable')
        btn.click()
        # while True:
        #     try:
        #
        #         break
        #     except ElementNotVisibleException as e:
        #         time.sleep(1)

        while True:
            try:
                download_btn = self._driver.find_element_by_xpath(config.get('savefrom.download.btn.xpath'))
                a_tag = self._driver.find_element_by_xpath(config.get('savefrom.download.a.tag.xpath'))
                file_name = a_tag.get_property('download')
                video_download_url = a_tag.get_property('href')
                base_store_dir = config.get('base.video.store.dir')
                if self._locale:
                    base_store_dir = os.path.join(base_store_dir, self._locale)
                store_dir = os.path.join(base_store_dir, self._page)
                if self._app_bag_name:
                    store_dir = os.path.join(store_dir, self._app_bag_name)
                store_dir = os.path.join(store_dir, 'video')
                store_dir = os.path.join(store_dir, self._post_id)
                if not os.path.exists(store_dir):
                    os.makedirs(store_dir)
                file_full_path = os.path.join(store_dir, file_name)
                if os.path.exists(file_full_path):
                    os.remove(file_full_path)

                get_logger().debug('retrieve video: ' + video_download_url)
                urllib.request.urlretrieve(video_download_url, file_full_path)
                get_logger().debug('download video done: ' + video_download_url)

                # action_chains = ActionChains(self._driver)
                # action_chains.key_down(Keys.LEFT_CONTROL).click(download_btn).key_up(Keys.LEFT_CONTROL)
                # action_chains.perform()

                # while True:
                #     if not os.path.exists(file_full_path):
                #         time.sleep(1)
                #     else:
                #         break

                break
            except NoSuchElementException as e:
                try:
                    result_box = self._driver.find_element_by_class_name('result-box')
                    if 'The download link not found' in result_box.text:
                        get_logger().debug('The download link not found: ' + video_url)
                        break
                except Exception as e2:
                    pass
                time.sleep(1)

        self._driver.quit()

    def download(self, video_url):
        if self._timeout_seconds and 'linux' == platform.system().lower():
            try:
                with time_limit(self._timeout_seconds):
                    self.__download__(video_url)
            except TimeoutException:
                self._driver.quit()
                print("time out")
        else:
            self.__download__(video_url)


if __name__ == '__main__':
    video_test_url = 'http://www.facebook.com/video/video.php?v=1803142173070710'
    x = 'https://www.facebook.com/SummonersWarCom2us/videos/164531474374114/'
    y = 'https://www.facebook.com/futbolmahou/videos/1687147074662341'
    VideoDownloader(page='SummonersWarCom2us', post_id='164531474374114').download(y)

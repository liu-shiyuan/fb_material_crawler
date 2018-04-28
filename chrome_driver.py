# -*- coding:utf-8 -*-
from selenium import webdriver
from config import *

chrome_driver_file_path = config.get('chromedriver.file')
default_download_path = config.get('base.video.store.dir')


def get_driver(store_path=None, locale=None):
    options = webdriver.ChromeOptions()
    if not store_path:
        _download_path = default_download_path
    else:
        _download_path = store_path
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': _download_path}
    if locale:
        prefs['intl.accept_languages'] = locale
    options.add_experimental_option('prefs', prefs)
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    if locale:
        options.add_argument('--lang=' + locale)
    if config.get('proxy.need') == 1:
        options.add_argument('--proxy-server=' + config.get('proxy.host') + ':' + str(config.get('proxy.port')))
    _driver = webdriver.Chrome(executable_path=chrome_driver_file_path, chrome_options=options)
    _driver.set_window_size(1200, 900)
    return _driver

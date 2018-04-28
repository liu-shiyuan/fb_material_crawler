# -*- coding:utf-8 -*-
from selenium import webdriver
from config import *


phantomjs_driver_file_path = config.get('phantomjs.driver.file')


def get_driver():
    _driver = webdriver.PhantomJS(phantomjs_driver_file_path)
    return _driver



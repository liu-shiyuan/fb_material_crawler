# -*- coding:utf-8 -*-
from common_fun import *
from PIL import Image
from config import *
import os


DEFAULT_SCREENSHOT__NAME = 'screenshot.png'


def take_banner_screenshot(driver, save_path):
    try:
        screenshot_file = os.path.join(save_path, DEFAULT_SCREENSHOT__NAME)
        driver.save_screenshot(screenshot_file)
        # _1dwg _1w_m _q7o
        target_ele = driver.find_element_by_class_name('_1w_m')
        print(target_ele.location)
        print(target_ele.size)

        left = target_ele.location['x']
        top = target_ele.location['y']
        right = target_ele.location['x'] + target_ele.size['width']
        bottom = target_ele.location['y'] + target_ele.size['height']

        im = Image.open(screenshot_file)
        im = im.crop((left, top, right, bottom))
        im.save(screenshot_file)
    except:
        pass


def take_carousel_screenshot(driver, save_path):
    try:
        take_banner_screenshot(driver, save_path)
    except:
        pass


if __name__ == '__main__':
    x = 'https://www.facebook.com/houseoffungames/posts/1831417040236479'

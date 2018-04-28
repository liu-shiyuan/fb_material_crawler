# -*- coding:utf-8 -*-
import os
import time


def __auto_setup__():
    while True:
        result = os.popen("ps -ef | grep mate").read()
        if 'material_crawler' in result:
            print(str(time.asctime()) + ': in progressing')
            time.sleep(60)
        else:
            print(str(time.asctime()) + ': restarting')
            result = os.system("nohup python3 material_crawler.py &")
            time.sleep(10)
            print('auto restart result:')
            print(os.popen("ps -ef | grep mate").read())


if __name__ == '__main__':
    __auto_setup__()
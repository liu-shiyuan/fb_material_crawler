# -*- coding:utf-8 -*-
import logging
import logging.config
import os

default_log_dir = 'logs'
if not os.path.exists(default_log_dir):
    os.mkdir(default_log_dir)
logging.config.fileConfig('./logger.conf')
__logger__ = logging.getLogger('fileLogger')
__record_logger__ = logging.getLogger('recordLogger')


def get_logger():
    return __logger__


def get_record_logger():
    return __record_logger__

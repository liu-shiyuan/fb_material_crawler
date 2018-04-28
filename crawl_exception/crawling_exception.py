# -*- coding:utf-8 -*-
class NotBannerException(Exception):
    def __init__(self, reason=None):
        self.reason = reason
        Exception.__init__(self)
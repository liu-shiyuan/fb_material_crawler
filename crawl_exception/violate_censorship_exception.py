# -*- coding:utf-8 -*-
class ViolateCensorshipException(Exception):
    def __init__(self, reason=None):
        self.reason = reason
        Exception.__init__(self)
# -*- coding:utf-8 -*-
import os
import configparser
import sys


class OperationalError(Exception):
    """"""


class Dictionary(dict):
    """ custom dict."""

    def __getattr__(self, key):
        return self.get(key, None)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Config:
    def __init__(self, file_name='init.conf'):
        self.env = {}
        for key, value in os.environ.items():
            self.env[key] = value

        config = configparser.ConfigParser()
        config_file = os.path.join(get_real_path(), file_name)
        if not os.path.exists(config_file):
            raise RuntimeError('config file not found: %s' % config_file)
        config.read(config_file)

        for section in config.sections():
            setattr(self, section, Dictionary())
            for name, raw_value in config.items(section):
                try:
                    # avoid '0' and '1' to be parsed as a bool value
                    if config.get(section, name) in ['0', '1']:
                        raise ValueError
                    value = config.getboolean(section, name)
                except ValueError:
                    try:
                        value = config.getint(section, name)
                    except ValueError:
                        value = config.get(section, name)
                self.env[name] = value

    def get(self, name):
        return self.env[name]


def get_real_path():
    arg_0 = sys.argv[0]
    arg_0 = os.path.abspath(arg_0)
    sap = '/'
    if arg_0.find(sap) == -1:
        sap = '\\'
    index = arg_0.rfind(sap)
    path = arg_0[:index] + sap
    return path


config = Config()

if __name__ == "__main__":
    print(config.get('chromedriver.file'))

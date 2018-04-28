# -*- coding:utf-8 -*-
import signal
from contextlib import contextmanager


class TimeoutException(Exception): pass


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


if __name__ == '__main__':
        try:
            with time_limit(15):
                print('')
        except TimeoutException:
            print('')
# -*- coding: utf-8 -*-
# @Author  : Smawe
# @Time    : 2023/3/25 14:35
# @File    : retry.py
# @Software: PyCharm

import functools
import time
import random
import logging
from ..exception import MaxRetryError


class Retrying(object):

    def __init__(self, func, stop_max_attempt_number=None, wait_random_min=None, wait_random_max=None):
        args = (func, stop_max_attempt_number, wait_random_min, wait_random_max)
        for i, v in enumerate(args):
            if callable(v):
                # 关键字传参
                if i == 0:
                    break

                if i == 1:
                    func, stop_max_attempt_number = stop_max_attempt_number, func
                    break
                elif i == 2:
                    func, stop_max_attempt_number, wait_random_min = wait_random_min, func, stop_max_attempt_number
                    break
                else:
                    # 位置传参时func在最后一个位置，进行位置互换
                    stop_max_attempt_number, wait_random_min, wait_random_max, func = \
                        func, stop_max_attempt_number, wait_random_min, wait_random_max
                    break

        if not callable(func):
            raise ValueError("func param error")
        functools.update_wrapper(self, func)
        self._func = func

        self._stop_max_attempt_number = stop_max_attempt_number if stop_max_attempt_number else 1

        self._wait_random_min = wait_random_min / 1000 if isinstance(wait_random_min, int) else 0
        self._wait_random_max = wait_random_max / 1000 if isinstance(wait_random_max, int) else 1
        if self._wait_random_max <= self._wait_random_min:
            raise ValueError("wait_random_min is greater than or equal to wait_random_max")

    def __call__(self, *args, **kwargs):
        current_retry_num = 0
        while True:
            if current_retry_num > self._stop_max_attempt_number:
                raise MaxRetryError("Exceeded maximum retry count error")
            try:
                if current_retry_num:
                    logging.info("\033[1;34mThis is currently the {} retry\033[0m".format(current_retry_num))
                    time.sleep(random.uniform(self._wait_random_min, self._wait_random_max))
                return self._func(*args, **kwargs)
            except:
                current_retry_num += 1


def retry(*args, **kwargs):
    return functools.partial(Retrying, *args, **kwargs)

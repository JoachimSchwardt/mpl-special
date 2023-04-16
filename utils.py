#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 11:08:46 2023

@author: joachim
"""

import time
import functools


__all__ = ['timer', 'add_cooldown']


def timer(func=None, dig=3):
    """Decorator:
    Print execution time of a function ('dig' == number of digits)."""
    if func is None:
        return functools.partial(timer, dig=dig)
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        time_start = time.perf_counter()
        result = func(*args, **kwargs)
        time_end = time.perf_counter()
        print(f"{func.__name__}: {(time_end - time_start)*1e3:.{dig}f}ms")
        return result
    return wrap


def add_cooldown(cooldown):
    """Decorator:
    Prevent execution of a function for 'cooldown' seconds: @add_cooldown(0.2)"""
    class CooldownWrapper:
        """Class keeping track of the time of the last function call"""
        def __init__(self, func):
            self.last_call_time = 0
            self.cooldown = cooldown
            self.func = func

        def __call__(self, *args, **kwargs):
            current_time = time.perf_counter()
            if current_time - self.last_call_time < self.cooldown:
                # ignore the function call
                return
            # do the function's work here
            result = self.func(*args, **kwargs)
            self.last_call_time = current_time
            return result

    def wrapper(func):
        return CooldownWrapper(func)

    return wrapper

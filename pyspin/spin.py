#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import sys
import time
from functools import wraps
from multiprocessing import Process, Queue


Box1 = u'⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
Box2 = u'⠋⠙⠚⠞⠖⠦⠴⠲⠳⠓'
Box3 = u'⠄⠆⠇⠋⠙⠸⠰⠠⠰⠸⠙⠋⠇⠆'
Box4 = u'⠋⠙⠚⠒⠂⠂⠒⠲⠴⠦⠖⠒⠐⠐⠒⠓⠋'
Box5 = u'⠁⠉⠙⠚⠒⠂⠂⠒⠲⠴⠤⠄⠄⠤⠴⠲⠒⠂⠂⠒⠚⠙⠉⠁'
Box6 = u'⠈⠉⠋⠓⠒⠐⠐⠒⠖⠦⠤⠠⠠⠤⠦⠖⠒⠐⠐⠒⠓⠋⠉⠈'
Box7 = u'⠁⠁⠉⠙⠚⠒⠂⠂⠒⠲⠴⠤⠄⠄⠤⠠⠠⠤⠦⠖⠒⠐⠐⠒⠓⠋⠉⠈⠈'
Spin1 = u'|/-\\'
Spin2 = u'◴◷◶◵'
Spin3 = u'◰◳◲◱'
Spin4 = u'◐◓◑◒'
Spin5 = u'▉▊▋▌▍▎▏▎▍▌▋▊▉'
Spin6 = u'▌▄▐▀'
Spin7 = u'╫╪'
Spin8 = u'■□▪▫'
Spin9 = u'←↑→↓'
Default = Box1


class Spinner(object):
    def __init__(self, frames):
        self.frames = frames
        self.length = len(frames)
        self.position = 0

    def current(self):
        return self.frames[self.position]

    def next(self):
        current_frame = self.current()
        if self.position == self.length - 1:
            self.reset()
        else:
            self.position = self.position + 1
        return current_frame.encode('utf-8')

    def reset(self):
        self.position = 0

    def animate(self, words='', interval=0.1):
        while(self.position != -1):
            print("\r{0}    {1}".format(self.next(), words), end="")
            time.sleep(interval)
            sys.stdout.flush()
        print("\n")


def make_spin(spin_style=Default, words=""):
    spinner = Spinner(spin_style)
    queue = Queue()

    def add_queue(func):
        @wraps(func)
        def wrapper():
            func()
            queue.put_nowait(1)
        return wrapper

    def decorator(func):
        @wraps(func)
        def wrapper():
            process = Process(target=add_queue(func))
            process.start()
            # If the func has some print message, print them first.
            time.sleep(0.2)
            while queue.empty():
                print("\r{0}    {1}".format(spinner.next(), words), end="")
                sys.stdout.flush()
                time.sleep(0.1)
            print('')
        return wrapper
    return decorator

# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

# clase core de las funciones nativas y alguna que otra función

import time



class ZynkNativeFunc:
    def __init__(self, func):
        self.func = func
    def call(self, interpreter, args):
        return self.func(args)
    def __repr__(self):
        return f"<native fn>"

def clock(args):
    return time.time()

nclock = ZynkNativeFunc(clock)

def add_natives(eval, funcs):
    for k, v in funcs.items():
        eval.env.define(k, v)

core_funcs = {"clock":nclock}
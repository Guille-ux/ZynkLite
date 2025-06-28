# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

class Stack:
    def __init__(self, push_func="cynkPush({value});", pop_func="cynkPop();", swap_func="cynkSwap();"):
        self.push_func=push_func
        self.pop_func=pop_func
        self.swap_func=swap_func
    def spush(self, val):
        return self.push_func.format(value=val)
    def spop(self):
        return self.pop_func[0:-1]
    def clean(self):
        pass
    def swap(self):
        return self.swap_func
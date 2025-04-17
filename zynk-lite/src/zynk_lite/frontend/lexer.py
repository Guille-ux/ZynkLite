# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

class ZynkLexer:
    def __init__(self, source):
        self.source = source
        self.current = 1
        self.column = 1
        self.line = 1
    def is_at_end(self):
        if self.current > len(self.source):
            return True
        return False
    def advance(self):
        if not self.is_at_end():
            self.current += 1
            self.column += 1
        return self.prev()
    def peek(self):
        if not self.is_at_end():
            return self.source[self.current]
    def prev(self):
        if not self.is_at_end():
            return self.source[self.current - 1]
    def match(self, expected):
        if self.peek()==expected:
            self.advance()
            return True
        return False
    def match_sequence(self, pattern):
        ret = self.current
        i = 0
        while not self.is_at_end():
            if self.prev(self.current)==pattern[i]:
                self.advance()
            else:
                self.current = ret
                return False
        return True
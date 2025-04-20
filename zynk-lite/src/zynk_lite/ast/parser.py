# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

from .. import tokens
from .. import errors

class AlgebraicParser:
    def __init__(self, tokens, debug=False):
        self.tokens = tokens
        self.debug = debug
        self.current = 0
    def is_at_end(self):
        return self.current >= len(tokens)
    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.tokens[self.current]
    def peek(self):
        if not self.is_at_end():
            return self.tokens[self.current+1]
        return None
    def eat(self, type):
        if self.peek().type == type:
            self.advance()
            return True
        return False


class ZynkLParser:
    def __init__(self, tokens, debug=False):
        self.debug = debug
        self.tokens = tokens
        self.current = 0
    def parse(self):
        pass
        # lógica para parsear
        # return parsed
    def is_at_end(self):
        return self.current >= len(tokens)
    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.tokens[self.current]
    def peek(self):
        if not self.is_at_end():
            return self.tokens[self.current+1]
        return None
    def eat(self, type):
        if self.peek().type == type:
            self.advance()
            return True
        return False

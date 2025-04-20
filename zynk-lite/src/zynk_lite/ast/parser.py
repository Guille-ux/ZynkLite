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
    def eat(self, tipo):
        if self.peek().type == tipo:
            self.advance()
            return True
        return False
    def prev(self):
        return self.tokens[self.current-1]
    def eat_more(*types):
        if self.peek().type in types:
            self.advance()
            return True
        return False
    def parse_logic(self):
        fnode = self.parse_comp()
        while self.eat_more(tokens.TokenType.AND, tokens.TokenType.OR, tokens.TokenType.XOR):
            pass
    def parse_comp(self):
        fnode = self.parse_expr()
        while self.eat_more(tokens.TokenType.EQUAL_EQUAL, tokens.TokenType.BANG_EQUAL, tokens.TokenType.LESS, tokens.TokenType.GREATER, tokens.TokenType.LESS_EQUAL, tokens.TokenType.GREATER_EQUAL):
            pass
    def parse_expr(self):
        fnode = self.parse_term()
        while self.eat_more(tokens.TokenType.PLUS, tokens.TokenType.MINUS):
            pass
    def parse_term(self):
        fnode = self.parse_factor()
        while self.eat_more(tokens.TokenType.STAR, tokens.TokenType.SLASH):
            pass

    def parse_factor(self):
        pass


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
    def prev(self):
        return self.tokens[self.current-1]
    def eat_more(*types):
        if self.peek().type in types:
            self.advance()
            return True
        return False

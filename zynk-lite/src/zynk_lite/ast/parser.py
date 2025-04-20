# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

from .. import tokens
from . import expressions as zexpr
from .. import errors

class AlgebraicParser: # tremend descenso recursivo
    def __init__(self, tokens, debug=False):
        self.tokens = tokens
        self.debug = debug
        self.current = 0
    def parse(self):
        return self.parse_logic()
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
            op = self.prev().lexem
            snode = self.parse_comp()
            fnode = zexpr.Binary(fnode, op, snode)
        return fnode
    def parse_comp(self):
        fnode = self.parse_expr()
        while self.eat_more(tokens.TokenType.EQUAL_EQUAL, tokens.TokenType.BANG_EQUAL, tokens.TokenType.LESS, tokens.TokenType.GREATER, tokens.TokenType.LESS_EQUAL, tokens.TokenType.GREATER_EQUAL):
            op = self.prev().lexem
            snode = self.parse_expr()
            fnode = zexpr.Binary(fnode, op, snode)
        return fnode
    def parse_expr(self):
        fnode = self.parse_term()
        while self.eat_more(tokens.TokenType.PLUS, tokens.TokenType.MINUS):
            op = self.prev().lexem
            snode = self.parse_term()
            fnode = zexpr.Binary(fnode, op, snode)
        return fnode
    def parse_term(self):
        fnode = self.parse_factor()
        while self.eat_more(tokens.TokenType.STAR, tokens.TokenType.SLASH):
            op=self.prev().lexem
            snode = self.parse_factor()
            fnode = zexpr.Binary(fnode, op, snode)
        return fnode

    def parse_factor(self):
        if self.eat_more(tokens.TokenType.MINUS, tokens.TokenType.BANG):
            op = self.prev().lexem
            return zexpr.Unary(op, self.parse_factor(self.actual()))
        elif self.eat_more(tokens.TokenType.STRING, tokens.TokenType.FLOAT, tokens.TokenType.BOOL, tokens.TokenType.NULL):
            return zexpr.Literal(self.prev.value)
        elif self.eat(tokens.TokenType.IDENTIFIER):
            if self.eat(tokens.TokenType.DOT):
                if self.eat(tokens.TokenType.IDENTIFIER):
                    return zexpr.MIdentifier(self.tokens[self.current-3].lexem, self.prev().lexem)
                else:
                    raise SyntaxError("Expected identifier after a dot")
            return zexpr.Identifier(self.prev().lexem)
        else:
            raise SyntaxError("Unexpected Token")
    def actual(self):
        return self.tokens[self.current]

# monte eso a escondidas a 4 am
# código clandestino


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
    def actual(self):
        return self.tokens[self.current]

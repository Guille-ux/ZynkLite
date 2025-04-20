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
        return self.current >= len(self.tokens)
    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.tokens[self.current]
    def peek(self):
        if self.current+1 < len(self.tokens):
            return self.tokens[self.current+1]
        return None
    def eat(self, tipo):
        if self.actual().type == tipo:
            self.advance()
            return True
        return False
    def prev(self):
        return self.tokens[self.current-1]
    def eat_more(self, *types):
        if self.actual().type in types:
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
            return zexpr.Unary(op, self.parse_factor())
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
    def is_at_end(self):
        return self.current >= len(self.tokens)
    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.tokens[self.current]
    def peek(self):
        if self.current+1 <= len(self.tokens):
            return self.tokens[self.current+1]
        return None
    def eat(self, tipe):
        if self.actual().type == tipe:
            self.advance()
            return True
        return False
    def prev(self):
        return self.tokens[self.current-1]
    def eat_more(self, *types):
        if self.actual().type in types:
            self.advance()
            return True
        return False
    def actual(self):
        return self.tokens[self.current]
    def parse_import(self):
        if self.eat_more(tokens.TokenType.IDENTIFIER, tokens.TokenType.STRING):
            first = self.algebraic([self.prev()])
            if self.eat(tokens.TokenType.AS):
                if self.eat_more(tokens.TokenType.IDENTIFIER, tokens.TokenType.STRING):
                    return zexpr.ImportExpr(first, self.algebraic([self.prev()]))
                else:
                    raise SyntaxError("Expected Identifier/String after as")
            else:
                return zexpr.ImportExpr(first, first) 
        else:
            raise SyntaxError("Expected Identifier/String After Import")
    def parse_identifier(self):
        first = self.prev()
        if self.eat(tokens.TokenType.DOT):
            if self.eat(tokens.TokenType.IDENTIFIER):
                return MIdentifier(first.lexem, self.prev().lexem)
            else:
                raise SyntaxError("Expected Identifier After dot")
        else:
            return zexpr.Identifier(self.prev().lexem)
    def algebraic(self, toks):
        psd = AlgebraicParser(toks, self.debug)
        return psd.scan()
    def parse(self):
        statements = []
        while not self.is_at_end():
            stmt = self.parse_stmt()
            if stmt is not None:
                statements.append(stmt)
        return statements
    def parse_stmt(self):
        tok = self.actual()
        if tok.type == tokens.TokenType.IMPORT:
            self.advance()
            return self.parse_import()
        elif tok.type == tokens.TokenType.IDENTIFIER:
            self.advance()
            first = self.parse_identifier()
            if self.eat(tokens.TokenType.EQUAL):
                expression = self.parse_expression()
                return zexpr.VarAssign(first.name, expression)
            else:
                raise SyntaxError("Unexpected Token after Identifier")
        elif tok.type == tokens.TokenType.IF:
           return self.parse_if()

        elif tok.type == tokens.TokenType.WHILE:
            return self.parse_while()

        elif tok.type == tokens.TokenType.FOR:
            return self.parse_for()

        elif tok.type == tokens.TokenType.FUNC:
            return self.parse_func()
        
        elif tok.type == tokens.TokenType.VAR:
            self.advance()
            if self.eat(tokens.TokenType.IDENTIFIER):
                name = self.prev().lexem
                if self.eat(tokens.TokenType.EQUAL):
                    value = self.parse_expression()
                    return zexpr.VarAssign(name, value)
                else:
                    return zexpr.VarAssign(name, zexpr.Literal(None))
            else:
                raise SyntaxError("Expected identifier after 'var'")
        elif tok.type == tokens.TokenType.LBRACE:
            self.advance()
            return self.parse_block()
        elif tok.type == tokens.TokenType.SEMICOLON:
            self.advance()
            return None
        elif tok.type == tokens.TokenType.EOF:
            return None
    def parse_expression(self):
        expr = []
        while not self.is_at_end():
            if self.eat(tokens.TokenType.SEMICOLON):
                break
            elif self.eat(tokens.TokenType.EOF):
                raise SyntaxError("Unexpected EOF")
            else:
                expr.append(self.actual())
                self.advance()
        return self.algebraic(expr)
    def parse_block(self):
        block = []
        while not self.is_at_end():
            if self.eat(tokens.TokenType.RBRACE):
                break
            elif self.eat(tokens.TokenType.EOF):
                raise SyntaxError("Unexpected EOF")
            else:
                block.append(self.actual())
                self.advance()
        subparse = ZynkLParser(block, self.debug)
        return subparse.parse()
    def parse_if(self):
        pass
    def parse_while(self):
        pass
    def parse_for(self):
        pass
    def parse_func(self):
        pass
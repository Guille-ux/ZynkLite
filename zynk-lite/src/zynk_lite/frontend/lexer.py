# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

from .. import errors
from .. import tokens

class ZynkLLexer:
    def __init__(self, source):
        self.source = source # código fuente
        self.current = 1 # posición actual + 1
        self.start = 0 # donde empieza el token actual
        self.line = 1
        self.column = 1
        self.error = False
        self.tokens = [] # tokens de salida
        self.var_set = "abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ_"
        # fin de lo necesario actualmente
    def is_at_end(self): # para saber si llegamos al final del código
        return self.current >= len(self.source)
    def peek(self): # obtener siguiente caracter
        if self.is_at_end():
            return "\0"
        return self.source[self.current]
    def prev(self):
        return self.source[self.current-1] # caracter previo
    def advance(self): # avanzer
        self.current += 1
        self.column += 1
        return self.source[self.current-1]
    def match(self, expected): # consumir si es el caracter esperado
        if self.is_at_end() or self.peek() != expected:
            return False
        self.current += 1
        self.column += 1
        return True
    def match_sequence(self, seq): # Identificar Patrones
        ret_point = self.current
        first = self.prev()
        if first != seq[0]:
            return False
        i = 1
        while i < len(seq) and not self.is_at_end():
            if not self.match(seq[i]):
                self.current = ret_point
                return False
            i += 1
        if self.peek() not in self.var_set:
            return True
        self.current = ret_point
        return False
    def add_token(self, tipo, lexem="", value=None):
        self.tokens.append(tokens.Token(tipo, lexem, value, self.line, self.column))
    # utilidades lvl. 1 acabadas
    
    # Utilidades lvl2
    def skip_comment(self):
        if self.prev()=="#":
            char = self.peek()
            while not self.is_at_end():
                if char == "\n":
                    break
                char = self.advance()
            return True
        return False
    def num_lexer(self):
        consumed = False
        while not self.is_at_end():
            char = self.advance()
            if consumed:
                if not char.isdigit():
                    self.current -= 1
                    break
            else:
                if char==".":
                    consumed = True
                elif char.isdigit():
                    pass
                else:
                    self.current -= 1
                    break
        return consumed
    def string_lex(self):
        start = self.current - 1
        while not self.is_at_end():
            char  = self.advance()
            if char == '"':
                break
        return self.source[start:self.current]
    def identifier_lex(self):
        start = self.current-1
        while not self.is_at_end():
            char = self.advance()
            if char not in self.var_set:
                self.current -= 1
                break
        return self.source[start:self.current]

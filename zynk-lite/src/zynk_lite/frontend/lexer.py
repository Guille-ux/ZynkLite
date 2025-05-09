# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

from .. import errors
from .. import tokens

class ZynkLLexer:
    def __init__(self, source, debug=False):
        self.debug = debug
        self.source = source # código fuente
        self.current = 0 # posición actual + 1
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
                    self.line += 1
                    self.column = 1
                    self.advance()
                    break
                char = self.advance()
            return True
        return False
    def num_lexer(self):
        consumed = False
        self.current -= 1
        self.column -= 1
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
            char = self.advance()
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
    
    # eso solo fueron utilidades, ahora llega el verdadero escaneo LEXER LVL 3

    def scan(self): # ESCANEO
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.add_token(tokens.TokenType.EOF) # añadir final de archivo al final
        return self.tokens
    def scan_token(self):
        char = self.advance()
        if self.skip_comment():
            pass
        elif char=="\n":
            self.column = 1
            self.line += 1
        elif char in ("\t", " ", "\r"):
            pass
        elif char=="(":
            self.add_token(tokens.TokenType.LPAREN, "(")
        elif char==")":
            self.add_token(tokens.TokenType.RPAREN, ")")
        elif char=="{":
            self.add_token(tokens.TokenType.LBRACE, "{") # ME ABURRO, es muy repetitivo
        elif char=="}":
            self.add_token(tokens.TokenType.RBRACE, "}")
        elif char=="[":
            self.add_token(tokens.TokenType.LBRACKET, "[")
        elif char=="]":
            self.add_token(tokens.TokenType.RBRACKET, "]")
        elif char==";":
            self.add_token(tokens.TokenType.SEMICOLON, ";") # SEMICOLON
        # VALORES
        elif char=='"': # String's
            lexem = self.string_lex()
            value = lexem[1:-1]
            self.add_token(tokens.TokenType.STRING, lexem, value)
        elif char.isdigit(): # numbers
            self.num_lexer()
            lexem = self.source[self.start:self.current]
            value = float(lexem)
            self.add_token(tokens.TokenType.FLOAT, lexem, value)
        
        # SIMBOLOS xD
        elif char=="*":
            self.add_token(tokens.TokenType.STAR, "*")
        elif char=="/":
            self.add_token(tokens.TokenType.SLASH, "/")
        elif char=="-":
            self.add_token(tokens.TokenType.MINUS, "-")
        elif char=="+":
            self.add_token(tokens.TokenType.PLUS, "+")
        elif char==":":
            self.add_token(tokens.TokenType.COLON, ":")
        elif char==".":
            self.add_token(tokens.TokenType.DOT, ".")
        elif char=="^":
            self.add_token(tokens.TokenType.XOR, "^")
        # de doble comprobación
        elif char=="!":
            if self.match("="):
                self.add_token(tokens.TokenType.BANG_EQUAL, "!=")
            else:
                self.add_token(tokens.TokenType.BANG, "!")
        elif char=="=":
            if self.match("="):
                self.add_token(tokens.TokenType.EQUAL_EQUAL, "==")
            else:
                self.add_token(tokens.TokenType.EQUAL, "=")
        elif char=="<":
            if self.match("="):
                self.add_token(tokens.TokenType.LESS_EQUAL, "<=")
            else:
                self.add_token(tokens.TokenType.LESS, "<")
        elif char==">":
            if self.match("="):
                self.add_token(tokens.TokenType.GREATER_EQUAL, ">=")
            else:
                self.add_token(tokens.TokenType.GREATER, ">")
        elif char==",":
        # BUILT-IN
            self.add_token(tokens.TokenType.COMMA, ",")
        elif self.match_sequence("import"):
            self.add_token(tokens.TokenType.IMPORT, "import")
        # Other Types
        elif self.match_sequence("null"):
            self.add_token(tokens.TokenType.NULL, "null")
        elif self.match_sequence("true"):
            self.add_token(tokens.TokenType.BOOL, "true", True)
        elif self.match_sequence("false"):
            self.add_token(tokens.TokenType.BOOL, "false", False)
        
        # Keywords
        elif self.match_sequence("func"):
            self.add_token(tokens.TokenType.FUNC, "func")
        elif self.match_sequence("var"):
            self.add_token(tokens.TokenType.VAR, "var")
        elif self.match_sequence("list"):
            self.add_token(tokens.TokenType.LIST, "list")
        elif self.match_sequence("call"):
            self.add_token(tokens.TokenType.CALL, "call")
        elif self.match_sequence("to"):
            self.add_token(tokens.TokenType.TO, "to")
        elif self.match_sequence("and"):
            self.add_token(tokens.TokenType.AND, "and")
        elif self.match_sequence("not"):
            self.add_token(tokens.TokenType.BANG, "not")
        elif self.match_sequence("or"):
            self.add_token(tokens.TokenType.OR, "or")
        elif self.match_sequence("while"):
            self.add_token(tokens.TokenType.WHILE, "while")
        elif self.match_sequence("for"):
            self.add_token(tokens.TokenType.FOR, "for")
        elif self.match_sequence("return"):
            self.add_token(tokens.TokenType.RETURN, "return")
        elif self.match_sequence("if"):
            self.add_token(tokens.TokenType.IF, "if")
        elif self.match_sequence("else"):
            self.add_token(tokens.TokenType.ELSE, "else")
        elif self.match_sequence("as"):
            self.add_token(tokens.TokenType.AS)
        elif char in self.var_set:
            self.add_token(tokens.TokenType.IDENTIFIER, self.identifier_lex())
        else:
            self.error = True
            lerror = self.throw("Unexpected Token")
            lerror.print_error()
            if self.debug:
                print(f"[!] {lerror} [!]")
    def throw(self, msg): # Ayuditas del pedro sánchez
        return errors.ZynkError(self.line, self.column, msg)
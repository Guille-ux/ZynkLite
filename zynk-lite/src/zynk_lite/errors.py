# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3
import sys

class ZynkError(Exception):
    def __init__(self, line, column, error):
        self.line =line
        self.column = column
        self.error = error
        self.msg = f"[line : {line}, column : {column}] : Error : {error}"
        super().__init__(self.msg)
    def print_error(self):
        print(self.msg, file=sys.stderr)
    def __str__(self):
        return self.msg
    def __repr__(self):
        return self.msg
    
class EvalError(ZynkError): # jajajja añadiendo un error nuevo, quien diria que hay que programar errores ¿no? xD
    def __init__(self, nexpr, error):
        self.nexpr = nexpr
        self.error = error
        self.column = None
        super().__init__(self.nexpr, self.column, self.error)

class ParserError(ZynkError): # otro tipo de error nuevo, luego añadire errores más especificos, de momento me es suficiente así, pensar que pare de hacer un lenguaje de programación para hacer otro, lo bueno es que ahora voy mucho más rápido
    def __init__(self, token, token_pos, error):
        self.token = token
        self.pos = token_pos
        self.error = error
        super().__init__(token, token_pos, error)
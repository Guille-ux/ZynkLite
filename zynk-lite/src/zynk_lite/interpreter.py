# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

from .frontend import lexer
from .ast import eval
from .ast import parser

class ZynkLInterpreter:
    def __init__(self, standard_lib_path=None, enclosing=None, debug=False, extension=".zl"):
        self.evaluator = eval.ZynkLEval(standard_lib_path, enclosing, debug, extension)
        self.debug = debug
    def eval(self, code):
        lex = lexer.ZynkLLexer(code, self.debug)
        tokens = lex.scan()
        par = parser.ZynkLParser(tokens, self.debug)
        parsed = par.parse()
        for stmt in parsed:
            self.evaluator.eval(stmt)
        if self.debug:
            print(tokens)
            print(parsed)
    def eval_file(self, filepath):
        with open(filepath, "r") as f:
            code = f.read()
        self.eval(code)
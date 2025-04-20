# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

from . import frontend.lexer as lexer
from . import ast.eval as eval
from . import ast.parser as parser

class Interpreter:
    def __init__(self, standard_lib_path=None, enclosing=None, debug=False, extension=".zl"):
        self.evaluator = eval.ZynkLEval(standard_lib_path, enclosing, debug, extension)
        self.debug = debug
    def eval(self, code):
        lex = lexer.ZynkLLexer(code, self.debug)
        tokens = lex.scan()
        par = parser.ZynkLParser(tokens, self.debug)
        parsed = par.parse()
        for stmt in parsed():
            self.evaluator.eval(stmt)
    def eval_file(self, filepath):
        with open(filepath, "r") as f:
            code = f.read()
        self.eval(code)
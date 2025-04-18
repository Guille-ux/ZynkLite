# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

from .. import errors
from . import expressions as expr

class Visitor:
    def __init__(self):
        raise NotImplementedError()

class ZynkLEval(Visitor): # tengo que decir que amo el patron del visitante, es maravilloso
    def __init__(self, debug=False):
        self.debug = debug
    def eval(self, expr):
        return expr.accept(self)
    def visit_literal(self, expr):
        return expr.value
    def visit_binary(self, expr):
        left = expr.left.accept(self)
        right = expr.right.accept(self)

        if expr.operand == "+":
            return left + right
        elif expr.operand == "*":
            return left * right
        elif expr.operand == "/":
            return left / right
        elif expr.operand == "-":
            return left - right
        elif expr.operand == "==":
            return left == right
        elif expr.operand == "<":
            return left < right
        elif expr.operand == ">":
            return left > right
        elif expr.operand == "<=":
            return left <= right
        elif expr.operand == ">=":
            return left >= right
        else:
            error = errors.EvalError(expr, f"Invalid Binary Operand '{expr.operand}'!")
            if self.debug:
                raise error
            error.print_error()
    def visit_unary(self, expr):
        operand = expr.operand
        right = expr.right

        if operand == "!":
            return not right
        elif operand == "-":
            return - right
        else:
            error = errors.EvalError(expr, f"Invalid Unary Operand {expr.operand}!")
            if self.debug:
                raise error
            error.print_error()

# sodio, yo montando un lenguaje de programación desde 0 para que tengais video xD, viva la república y viva la Asexualidad! :)
# realmente no creo que sea sano programar de 23:54 hasta 05:00 creo que deberia dormir más, pero bueno, programar es programar!
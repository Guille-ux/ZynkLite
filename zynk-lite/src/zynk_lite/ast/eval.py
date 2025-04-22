# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

from .. import errors
from . import expressions as zexpr
from . import zenv
from ..frontend import lexer
from . import parser
import os
from pathlib import Path
from ..native_funcs import core

class Visitor:
    def __init__(self):
        raise NotImplementedError()

class ZynkLEval(Visitor): # tengo que decir que amo el patron del visitante, es maravilloso
    def __init__(self, standard_lib_path=None, enclosing=None, debug=False, extension=".zl"):
        self.extension = extension
        self.debug = debug
        self.ret = None
        self.env = zenv.Enviroment(enclosing)
        if standard_lib_path is None:
            project_root = Path(__file__).resolve().parent.parent
            self.stdlib_path = project_root / "lib"
        else:
            self.stdlib_path = standard_lib_path
        core.add_natives(self, core.core_funcs)
        self._module_cache = {}
    def subenv(self):
        new = zenv.Enviroment(self.env)
        return new
    def new_subenv(self):
        self.switch(self.subenv())
    def switch(self, env):
        self.env = env
    def undo(self):
        self.env = self.env.enclosing
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
        right = self.eval(expr.right)

        if operand == "!":
            return not right
        elif operand == "-":
            return - right
        else:
            error = errors.EvalError(expr, f"Invalid Unary Operand {expr.operand}!")
            if self.debug:
                raise error
            error.print_error()
    def visit_grouping(self, expr):
        return expr.expression.accept(self)
    def visit_var_definition(self, expr):
        self.env.define(expr.name, self.eval(expr.expression))
        return None
    def visit_identifier(self, expr):
        return self.env.get(expr.name)
    def visit_func_definition(self, expr):
        function = zexpr.ZynkFunc(expr)
        self.env.define(expr.name, function)
        return None
    def visit_call_function(self, expr):
        fname = expr.name.name
        if isinstance(expr.name, zexpr.MIdentifier):
            self.switch(self.env.get(expr.name.module).env)
        function = self.env.get(fname)
        if not hasattr(function, "call"):
            raise RuntimeError(f"Error : '{fname} is not a function!")
        args = []
        for arg in expr.args:
            args.append(self.eval(arg))
        ret = function.call(self, args)
        if isinstance(expr.name, zexpr.MIdentifier):
            self.undo()
        self.env.assign(expr.to, ret)
        return None
    def visit_block(self, expr):
        self.new_subenv()
        try:
            result = None
            for stmt in expr.body:
                result = self.eval(stmt)
            return result
        finally:
            self.undo()
    def visit_if(self, expr):
        if self.eval(expr.condition):
            return self.eval(expr.then)
        elif expr.else_branch is not None:
            return self.eval(expr.else_branch)
        return None
    def visit_while(self, expr):
        while self.eval(expr.condition):
            self.eval(expr.body)
        return None
    def visit_print(self, expr):
        value = self.eval(expr.expression)
        print(value)
        return None
    def visit_input(self, expr):
        prompt = ""
        if expr.expression is not None:
            prompt = str(self.eval(expr.expression))
        t = input(prompt)
        self.env.assign(expr.to, t)
        return t
    def visit_import(self, expr): # esto a sido una tortura
        cwdir = os.getcwd()
        filename = self.eval(expr.name) + self.extension
        if self.debug:
            print(f"[+] Trying to Load {self.eval(expr.name)} from current work dir [+]")
        if filename in os.listdir():
            filepath = os.path.join(cwdir, filename)
            if os.path.isfile(filepath):
                if self.debug:
                    print(f"[+] Loading module {self.eval(expr.name)} from {filepath} [+]")
            else:
                raise RuntimeError(f"Error : {filepath} is not a file")
        else:
            if self.debug:
                print("[+] Trying to Load from Standard Library [+]")
            filepath = os.path.join(self.stdlib_path, filename)
        if filepath in self._module_cache:
            module = self._module_cache[filepath]
            self.env.define(self.eval(expr.alias), module)
            if self.debug:
                print("[+] Module Loaded From Cache [+]")
            return None
        with open(filepath, "r") as f:
            if self.debug:
                print(f"[+] Loading {self.eval(expr.name)} from {filepath} [+]")
            lex = lexer.ZynkLLexer(f.read(), self.debug)
            tokens = lex.scan()
            if self.debug:
                print(f"[+] Analysis of {expr.name} module completed [+]")
            pars = parser.ZynkLParser(tokens, self.debug)
            parsed = pars.parse()
            if self.debug:
                print(f"[+] Module Parsed [+]")
                print(f"[+] Evaluating [+]")
            self.new_subenv()
            for expression in parsed:
                self.eval(expression)
            module = zexpr.Module(self.eval(expr.name), self.env)
            self.undo()
            self.env.define(self.eval(expr.alias), module)
            self._module_cache[filepath] = module
            return None

    def visit_for(self, expr):
        self.new_subenv()
        self.eval(expr.initialized)
        while self.eval(expr.condition):
            self.eval(expr.body)
            self.eval(expr.increment)
        return None
    def visit_var_assign(self, expr):
        self.env.assign(expr.name, self.eval(expr.expression))
        return None
    def visit_return(self, expr):
        self.ret = self.eval(expr.expression)
        return self.ret
    def visit_array_expr(self, expr):
        return [self.eval(element) for element in expr.items]
    def visit_index_expr(self, expr):
        array = self.eval(expr.array)
        index = self.eval(expr.index)
        print(array)
    
    # Validaciones
        if not isinstance(array, list):
            raise errors.EvalError(expr, f"Expected array, got {type(array)}")
        try:
            index = int(index)
        except (TypeError, ValueError):
            raise errors.EvalError(expr, f"Array index must be integer, got {type(index)}")
    
        try:
            return array[index]
        except IndexError:
            raise errors.EvalError(expr, f"Index {index} out of bounds")

    def visit_index_assign_expr(self, expr):
        array = self.eval(expr.array)
        index = self.eval(expr.index)
        value = self.eval(expr.value)
        print(array)
    
        if not isinstance(array, list):
            raise errors.EvalError(expr, f"Expected array, got {type(array)}")
        try:
            index = int(index)
        except (TypeError, ValueError):
            raise errors.EvalError(expr, f"Array index must be integer, got {type(index)}")
    
        try:
            array[index] = value
            return value
        except IndexError:
            raise errors.EvalError(expr, f"Index {index} out of bounds")
        
    # wow, añadi muchos metodos, me falta algo para arrays, aunque eso tambien en el lexer y expresiones deberia montar bucles for pues todavia no existen tambien algo para imports
    # esto es sencillo, creo que más tarde copiare esto pero en vez de interpretar que compile, estaria bien, de paso uso patrones de diseño
    # el funcionamiento de ZynkLite va a hacer que me replantee mejoras en ZynkPy


# sodio, yo montando un lenguaje de programación desde 0 para que tengais video xD, viva la república y viva la Asexualidad! :)
# realmente no creo que sea sano programar de 23:54 hasta 05:00 creo que deberia dormir más, pero bueno, programar es programar!
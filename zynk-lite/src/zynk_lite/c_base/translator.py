# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

from ..ast import eval, expressions, zenv, parser
from .. import tokens
from .. import errors
from . import initialize # plantillas para inicialización de recursos, bueno, en realidad de eso se encarga templates
from . import stack
from . import mem
from . import funcs


class Cynk(eval.ZynkLEval): # C Transpiler for Zynk
    def __init__(self, std_path=None, enclosing=None, debug=False, extension=".zl"):
        super().__init__(std_path, enclosing, debug, extension)
        self.code = []
        self.context = ""
        self.temp_count = 0
        self.prefix="zynk_func"
        self.stack=stack.Stack() # usamos las por defecto
        self.tables = mem.MemoryManager()
        self.fmaker = funcs.FuncMk(self)
        self.program_header = initialize.InitProgram(self)
    def eval(self, expression):
        expression.accept(self)
    def seval(self, expr):
        expr.accept(self)
        self.code.append(self.context)
        return self.code
    def emit_ctx(self, context):
        self.code.append(context)
        self.context = ""
    def emit_c(self):
        self.emit_ctx(self.context)
    def pop_ctx(self):
        try:
            return self.context
        finally:
            self.context=""
    def emit(self, line):
        self.context += line + "\n"
    def visit_literal(self, expr):
        if expr.value==None:
            self.emit(self.stack.spush("zynkNull()"))
        elif isinstance(expr.value, bool):
            self.emit(self.stack.spush(f"zynkBool({str(expr.value).lower()})"))
        elif isinstance(expr.value, str):
            self.emit(self.stack.spush(f'zynkCreateString(&sysarena, "{expr.value}")'))
        elif isinstance(expr.value, float):
            self.emit(self.stack.spush(f"zynkNumber({expr.value})"))
        elif isinstance(expr.value, list):
            self.emit(self.stack.spush(f"zynkCreateArray(&sysarena, {len(expr.value)})"))
    def visit_binary(self, expr):
        expr.right.accept(self)
        expr.left.accept(self)
        if expr.operand=="-":
            self.emit(self.stack.spush(f"zynkValuesSub({self.stack.spop()}, {self.stack.spop()})"))
        elif expr.operand=="+":
            self.emit(self.stack.spush(f"zynkValuesAdd({self.stack.spop()}, {self.stack.spop()})"))
        elif expr.operand=="*":
            self.emit(self.stack.spush(f"zynkValuesMul({self.stack.spop()}, {self.stack.spop()})"))
        elif expr.operand=="/":
            self.emit(self.stack.spush(f"zynkValuesDiv({self.stack.spop()}, {self.stack.spop()})"))
        elif expr.operand=="==":
            self.emit(self.stack.spush(f"zynkBool(zynkValuesEqual({self.stack.spop()}, {self.stack.spop()}))"))
        elif expr.operand=="<":
            self.emit(self.stack.spush(f"zynkBool(zynkValuesLess({self.stack.spop()}, {self.stack.spop()}))"))
        elif expr.operand==">":
            self.emit(self.stack.spush(f"zynkBool(zynkValuesGreater({self.stack.spop()}, {self.stack.spop()}))"))
        elif expr.operand=="<=":
            self.emit(self.stack.spush(f"zynkBool(zynkValuesLessEqual({self.stack.spop()}, {self.stack.spop()}))"))
        elif expr.operand==">=":
            self.emit(self.stack.spush(f"zynkBool(zynkValuesGreaterEqual({self.stack.spop()}, {self.stack.spop()}))"))
        elif expr.operand=="and":
            self.emit(self.stack.spush(f"zynkBool(zynkValuesAnd({self.stack.spop()}, {self.stack.spop()}))"))
        elif expr.operand=="or":
            self.emit(self.stack.spush(f"zynkBool(zynkValuesOr({self.stack.spop()}, {self.stack.spop()}))"))
        elif expr.operand=="^":
            self.emit(self.stack.spush(f"zynkBool(zynkValuesXor({self.stack.spop()}, {self.stack.spop()}))"))
        elif expr.operand=="!=":
            self.emit(self.stack.spush(f"zynkBool(zynkValuesNotEqual({self.stack.spop()}, {self.stack.spop()}))"))
        else:
            error = errors.EvalError(expr, f"Invalid Binary Operand {expr.operand}")
            if self.debug:
                raise error
            error.print_error()
    def visit_unary(self, expr):
        operand = expr.operand
        right=expr.right.accept(self)

        if operand=="-":
            self.emit(self.stack.spush(f"zynkNumber(-{self.stack.spop()}.as.number)"))

        elif operand=="!":
            self.emit(self.stack.spush(f"zynkBool(zynkValuesNot({self.stack.spop()}))"))
        else:
            error = errors.EvalError(expr, f"Invalid Unary Operand {operand}!")
            if self.debug:
                raise error
            error.print_error()
    def visit_var_definition(self, expr):
        expr.expression.accept(self)
        self.emit(self.tables.emit_new(expr.name, self.stack))
    def visit_identifier(self, expr):
        self.emit(self.tables.emit_pget(expr.name, self.stack))
    def visit_func_definition(self, expr):
        self.program_header.add(self.fmaker.emit_func(expr))
        ret = self.stack.spush(f"zynkCreateNativeFunction(&sysarena, {expr.name}, (ZynkFuncPtr){self.prefix}_{expr.name})") + "\n" + "\t"
        ret += self.tables.emit_new(expr.name, self.stack)
        self.emit(ret)
    def visit_call_function(self, expr):
        self.emit("{")
        self.emit(f"Value __tmp__=zynkCreateArray(&sysarena, {len(expr.args)});")
        for arg in expr.args:
            arg.accept(self)
            self.emit(f"zynkArrayPush(&sysarena, __tmp__, {self.stack.spop()});")
        self.emit(self.stack.spush(f'zynkCallFunction(&sysarena, env, "{expr.name.name}", __tmp__)'))
        if expr.to is not None:
            self.emit(self.tables.emit_set(expr.to, self.stack))
        self.emit("}")
    def visit_grouping(self, expr):
        return self.eval(expr)
    def visit_block(self, expr, origin=True):
        self.emit_c()
        if origin:
            self.emit(self.tables.emit_nenv())
        for stmt in expr.body:
            self.eval(stmt)
        if origin:
            self.emit(self.tables.emit_ret_env())
    def visit_if(self, expr):
        self.eval(expr.condition)
        self.emit(f"if ({self.stack.spop()}.as.boolean)" + " {\n")
        self.eval(expr.then)
        self.emit("}\n")
        if expr.else_branch is not None:
            self.emit("else {\n")
            self.visit_block(expr.else_branch)
            self.emit("}\n")
    def visit_while(self, expr, origin=True):
        if origin:
            self.emit(self.tables.emit_nenv())
        self.eval(expr.condition)
        self.emit(f"while ({self.stack.spop()}.as.boolean)" + "{\n")
        self.visit_block(expr.body, origin=False)
        self.eval(expr.condition)
        self.emit("}\n")
        if origin:
            self.emit(self.tables.emit_ret_env())
    def visit_for(self, expr):
        self.eval(self.tables.emit_nenv())
        self.eval(expr.initialized)
        expr.body.append(expr.increment)
        self.visit_while(expr, origin=False)
        self.eval(self.tables.emit_ret_env())
    def visit_return(self, expr):
        self.eval(expr.expression)
        self.emit(self.tables.emit_ret_env())
        self.emit(f"return {self.stack.spop()};\n")
    def visit_array_expr(self, expr):
        self.emit("{")
        self.emit(f"Value __tmp__ = zynkCreateArray(&sysarena, {len(expr.items)});")
        for item in expr.items:
            self.eval(item)
            self.emit(f"zynkArrayPush(&sysarena, __tmp__, {self.stack.spop()});")
        self.emit(self.stack.spush("__tmp__"))
        self.emit("}\n")
    def visit_break(self, expr):
        self.emit("break;")
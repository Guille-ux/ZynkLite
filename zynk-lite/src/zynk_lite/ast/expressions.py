# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

# clase base para definir expresiones

from . import zenv
from .. import errors

class Expr:
    def __init__(self):
        raise NotImplementedError()
    def accept(self, visitor):
        raise NotImplementedError()
    def __str__(self):
        raise NotImplementedError()
    def __repr__(self):
        return self.__str__()
    
# Literal con patron del visitante, WoW

class Literal(Expr):
    def __init__(self, value):
        self.value = value
    def accept(self, visitor):
        return visitor.visit_literal(self)
    def __str__(self):
        return f"[ Literal : {self.value} ]"

# Operador Binario

class Binary(Expr):
    def __init__(self, left, operand, right):
        self.right = right
        self.left = left
        self.operand = operand
    def accept(self, visitor):
        return visitor.visit_binary(self)
    def __str__(self):
        return f"[ Binary : {self.left} : {self.operand} : {self.right} ]"
    
# Operador Unario

class Unary(Expr):
    def __init__(self, operand, right):
        self.right = right
        self.operand = operand
    def accept(self, visitor):
        return visitor.visit_unary(self)
    def __str__(self):
        return f"[ Unary : {self.operand} : {self.right} ]"
    
# Unos bonitos parentesis :)

class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression
    def accept(self, visitor):
        return visitor.visit_grouping(self)
    def __str__(self):
        return f"[ Grouping : {self.expression} ]"
    
# |--------------------------------------------------------|
# | Fin de las expresiones, ahora son sentencias           |
# | Guillermo Leira Temes 2:51 a.m. 18/4/2025              |
# |--------------------------------------------------------|

class PrintStmt(Expr):
    def __init__(self, expression):
        self.expression = expression
    def accept(self, visitor):
        return visitor.visit_print(self)
    def __str__(self):
        return f"[ Print : {self.expression} ]"
    
class InputStmt(Expr):
    def __init__(self, expression, to):
        self.expression = expression
        self.to = to
    def accept(self, visitor):
        return visitor.visit_input(self)
    def __str__(self):
        return f"[ Input : {self.expression} ]"
    

class VarDef(Expr):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
    def accept(self, visitor):
        return visitor.visit_var_definition(self)
    def __str__(self):
        return f"[ Var Definition : {self.name} : {self.expression} ]"
class VarAssign(VarDef):
    def accept(self, visitor):
        return visitor.visit_var_assign(self)
    def __str__(self):
        return f"[ Var Assign : {self.name} : {self.expression} ]"
        
class Identifier(Expr): # lo usare para cargar cosas en memeoria bajo un nombre
    def __init__(self, name):
        self.name = name
    def accept(self, visitor):
        return visitor.visit_identifier(self)
    def __str__(self):
        return f"[ Identifier : {self.name} ]"
    
class FuncDef(Expr):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body
    def accept(self, visitor):
        return visitor.visit_func_definition(self)
    def __str__(self):
        return f"[ Func Definition : {self.name} : {self.params} : {self.body} ]"
    
class CallFunc(Expr):
    def __init__(self, name, args, to=None):
        self.name = name # donde demonios se guarda
        self.args = args
        self.to = to
    def accept(self, visitor):
        return visitor.visit_call_function(self)
    def __str__(self):
        return f"[ Call : {self.name} : {self.args} : {self.to} ]"
    
class IfExpr(Expr):
    def __init__(self, condition, then, else_branch):
        self.condition = condition
        self.then = then
        self.else_branch = else_branch
    def accept(self, visitor):
        return visitor.visit_if(self)
    def __str__(self):
        return f"[ If : {self.condition} : {self.then} : {self.else_branch} ]"

class ImportExpr(Expr):
    def __init__(self, name, alias):
        self.name = name
        self.alias = alias
    def accept(self, visitor):
        return visitor.visit_import(self)
    def __str__(self):
        return f"[ Import : {self.name} ]"

class WhileExpr(Expr):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def accept(self, visitor):
        return visitor.visit_while(self)
    def __str__(self):
        return f"[ While : {self.condition} : {self.body} ]"
    
class ForExpr(Expr):
    def __init__(self, inited, inc, condition, body):
        self.initialized = inited
        self.condition = condition
        self.increment = inc
        
        self.body = body
    def accept(self, visitor):
        return visitor.visit_for(self)
    def __str__(self):
        return f"[ For : {self.initialized} : {self.condition} : {self.increment} : {self.body} ]"
    
class BlockExpr(Expr): # casí me olvido de añadir esto, parece insignificante, pero mejora todo muchisimo
    def __init__(self, body):
        self.body = body
    def accept(self, visitor):
        return visitor.visit_block(self)
    def __str__(self):
        return f"[ Block : {self.body} ]"
    
class ZynkFunc:
    def __init__(self, declaration):
        self.declaration = declaration
    def call(self, interpreter, args):
        env = interpreter.subenv()

        for i in range(len(self.declaration.params)):
            env.define(self.declaration.params[i], args[i])
        interpreter.switch(env)
        interpreter.eval(self.declaration.body)
        try:
            return interpreter.ret
        finally:
            interpreter.ret = None
            interpreter.undo()

class Module:
    def __init__(self, name, env):
        self.name = name
        self.env = env

class MIdentifier(Identifier):
    def __init__(self, module, name):
        self.module = module
        super().__init__(name)
    def accept(self, visitor):
        visitor.switch(visitor.env.get(self.module).env)
        try:
            return super().accept(visitor)
        finally:
            visitor.undo()
    def __str__(self):
        return f"[ Module : {self.module} : [ {self.name} ] ]"

class ReturnExpr(Expr):
    def __init__(self, expression):
        self.expression = expression
    def accept(self, visitor):
        return visitor.visit_return(self)
    def __str__(self):
        return f"[ Return : {self.expression} ]"

class ArrayExpr(Expr): # Ho Ho, ya llegan
    def __init__(self, elements):
        self.items = elements
    def accept(self, visitor):
        return visitor.visit_array_expr(self)
    def __str__(self):
        return f"[ Array : {self.items} ]"
    
class IndexExpr(Expr):
    def __init__(self, array, index):
        self.array = array # un array xD
        self.index = index # posición, espera, porque lo digo. acaso no sabes ingés?
    def accept(self, visitor):
        return visitor.visit_index_expr(self)
    def __str__(self):
        return f"[ Index : {self.index} : {self.array} ]"

class IndexAssignExpr(Expr):
    def __init__(self, array, index, value):
        self.array = array
        self.index = index
        self.value = value
    def accept(self, visitor):
        return visitor.visit_index_assign_expr(self)
    def __str__(self):
        return f"[ Assign Index : {self.value} : {self.index} : {self.array} ]"


# FUTURO ¿?
"""
class ArrayDef(Expr):
    pass.....


class ArrayGet(Expr):
    pass......

    
class Struct(Expr):
    pass......

    
class DefStruct(Expr):
    pass.......

    
"""

# Bueno, esta es mi pequeña implementación actual de expresiones para ZynkLite
# Espero que te haya gustado, pues lo escribi a las 3:21 del 18/4/2025
# No se cuando estaras leyendo esto, pero Gracias ;)
# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

# clase base para definir expresiones

class Expr:
    def __init__(self):
        raise NotImplementedError()
    def accept(self, visitor):
        raise NotImplementedError()
    def __str__(self):
        raise NotImplementedError()
    
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
    def __init__(self, expression):
        self.expression = expression
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
        self.name = name
        self.args = args
        self.to = to
    def accept(self, visitor):
        return visitor.visit_call_function(self)
    def __str__(self):
        return f"[ Call : {self.name} : {self.args} : {self.to} ]"
    
class IfExpr:
    def __init__(self, condition, then, else_branch=None):
        self.condition = condition
        self.then = then
        self.else_branch = else_branch
    def accept(self, visitor):
        return visitor.visit_if(self)
    def __str__(self):
        return f"[ If : {self.condition} : {self.then} : {self.else_branch} ]"

class ImportExpr(Expr):
    def __init__(self, name):
        self.name = name
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
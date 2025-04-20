# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

class Enviroment: # importante, diferente contexto => diferente resultado
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing
    def define(self, name, value):
        self.values[name]=value
    def get(self, name):
        if name in self.values:
            return self.values[name]
        elif self.enclosing is not None:
            return self.enclosing.get(name)
        return RuntimeError(f"Error '{name}' not defined!")
    def assign(self, name, value):
        if name in self.values:
            self.values[name] = value
        elif self.enclosing is not None:
            self.enclosing.assign(name, value)
        return RuntimeError(f"Error'{name}' not defined!")

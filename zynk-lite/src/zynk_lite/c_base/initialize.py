# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

from . import *
from .. import tokens, errors
from ..ast import *

class InitProgram:
    def __init__(self, trans):
        self.trans=trans
        self.headers= """
        // Headers Generated with InitProgram class from zynk_lite/c_base/initialize.py

        """

    def add(self, line):
        self.headers+=line+"\n"
    def add_func(self, fname): # para añadir las declaraciones, xD
        self.add(f"Value {self.trans.prefix}_{fname}(ArenaManager *manager, ZynkEnv *env, ZynkArray *args);")
    def emit(self):
        return self.headers

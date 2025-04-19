# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

from .. import tokens
from .. import errors

class AlgebraicParser:
    def __init__(self, tokens, debug=False):
        self.tokens = tokens
        self.debug = debug

class ZynkLParser:
    def __init__(self, tokens, debug=False):
        self.debug = debug
        self.tokens = tokens
    def parse(self):
        # lógica para parsear
        # return parsed 
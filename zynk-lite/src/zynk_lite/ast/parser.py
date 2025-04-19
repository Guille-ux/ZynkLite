# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

from .. import tokens
from .. import errors

class ZynkLParser:
    def __init__(self, tokens, debug):
        self.debug = debug
        self.tokens = tokens
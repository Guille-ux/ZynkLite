# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3
import sys

class ZynkError(Exception):
    def __init__(self, line, column, error):
        self.line =line
        self.column = column
        self.error = error
        self.msg = f"[line : {line}, column : {column}] : Error : {error}"
        super().__init__(self.msg)
    def print_error(self):
        print(self.msg, file=sys.stderr)
    def __str__(self):
        return self.msg
    def __repr__(self):
        return self.msg
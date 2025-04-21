# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

from src.zynk_lite import interpreter as intp
interpreter = intp.ZynkLInterpreter(debug=True)
case = """
var x;
input "nose " to x;
print x;
"""
interpreter.eval(case)
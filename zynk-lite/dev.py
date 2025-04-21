# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

from src.zynk_lite import interpreter as intp
interpreter = intp.ZynkLInterpreter(debug=True)
case = """
var i;
var ini;
var end;

call clock() to ini;

var count=0;
while (count < 100000) {
  count = count + 1;
}

call clock() to end;

print "Tiempo de ejecución:";
print end - ini;

"""
interpreter.eval(case)
# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from src.zynk_lite import interpreter as intp
interpreter = intp.ZynkLInterpreter(debug=True)
case = """
func isAdult(age) {
	if (age >= 18) {
		return true;
	} else {
		return false;
	}
}

var r;
call isAdult(16) to r;
print r;

var h = [2, 3];
print h;
call push (h, 3);
print h;

call write("ns.txt", "hola");

"""
interpreter.eval(case)

# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

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

"""
interpreter.eval(case)
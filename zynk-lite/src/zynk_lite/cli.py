# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

from . import interpreter as intp
from . import compiler
import sys

def main():
    if sys.argv[1]=="run":
        filepath = sys.argv[2]
        interpreter = intp.ZynkLInterpreter()
        interpreter.eval_file(filepath)
    # muchas más opciones
    elif sys.argv[1]=="cli":
        print("[+] ZynkLite Interpreter 0.0.10 [+]")
        print("[*] Type 'quit' or 'exit' to close [*]")
        interpreter = intp.ZynkLInterpreter()
        while True:
            opt = input(">>> ")
            if opt=="quit" or opt=="exit":
                break
            interpreter.eval(opt)
        print("[-] ZynkLite Terminated [-]")
    else:
        print("[!] BAD USAGE → zynkl [run/cli] [file] [!]")
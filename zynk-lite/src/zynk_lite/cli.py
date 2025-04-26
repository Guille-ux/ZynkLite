# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

from . import interpreter as intp
from . import compiler
from . __about__ import __version__ as version
import sys


def main():
    if sys.argv[1]=="run":
        filepath = sys.argv[2]
        interpreter = intp.ZynkLInterpreter()
        interpreter.eval_file(filepath)
    # muchas más opciones
    elif sys.argv[1]=="cli":
        print(f"[+] ZynkLite Interpreter {version} [+]")
        print("[*] Type 'quit' or 'exit' to close [*]")
        interpreter = intp.ZynkLInterpreter()
        while True:
            opt = input(">>> ")
            if opt=="quit" or opt=="exit":
                break
            try:
                interpreter.eval(opt)
            except Exception as e:
                print(f"[!] Error: {e} [!]")
        print("[-] ZynkLite Terminated [-]")
    else:
        print("[!] BAD USAGE → zynkl [run/cli] [file] [!]")

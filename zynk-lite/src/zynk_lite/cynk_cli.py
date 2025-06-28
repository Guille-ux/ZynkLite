# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

from . import *
import sys
import os
import time

def cynk_help():
    print("[ Use : cynk -s [source files] -o [out file] -i [includes] ]")
    print("[ Example : cynk -s my_program.zl -o my_program.c ]")
    print("[ Options ]")
    print("[ -s : source file ]")
    print("[ -o : out file ]")
    print("[ -i : files included ]")
    print("[ -v : sets the debug flag of the transpiler ]")

def main():
    help_flag=False
    source = None
    includes = []
    out_file = "out.c"
    debug=False
    alone=False
    if "--standalone" in sys.argv:
        sys.argv.remove("--standalone")
        alone=True
    if len(sys.argv) < 2:
        print("[ Error, at least 1 arg is needed, type with --help or with -h ]")
    arg_index=0
    while arg_index < len(sys.argv):
        arg=sys.argv[arg_index]
        if arg=="--help" or arg=="-h":
            help_flag=True
            break
        elif arg=="-s":
            arg_index+=1
            if arg_index >= len(sys.argv):
                raise Exception("[ Expected arg after '-s' ]")
            arg=sys.argv[arg_index]
            source = arg[:]
        elif arg=="-o":
            arg_index+=1
            if arg_index >= len(sys.argv):
                raise Exception("[ Expected arg after '-o' ]")
            arg=sys.argv[arg_index]
            out_file = arg[:]
        elif arg=="-i":
            while arg[0]!="-" and arg_index < len(sys.argv):
                arg=sys.argv[arg_index]
                includes.append(arg)
                arg_index+=1
            if arg[0]=="-":
                continue
        elif arg=="-v":
            debug=True
        arg_index+=1
    if help_flag:
        cynk_help()
    elif source is not None:
        if alone:
            config = {"a_or_b":"STANDALONE"}
        else:
            config = {"a_or_b":"ANSI"}
        config["output_filename"] = out_file
        start = time.time()
        trans = transpiler.Transpiler(config=config, debug=debug)
        with open(source, "r") as f:
            source_code = f.read()
        code = trans.transpile(source_code, includes)
        with open(out_file, "w") as f:
            f.write(code)
        final=time.time()
        print(f"[ Finnish in {final-start}'s ]")
    else:
        cynk_help()


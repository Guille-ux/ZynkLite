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
    print("[ --stack-max : sets the max stack capacity ]")
    print("[ --table-max : sets the max table capacity ]")
    print("[ --index-type : sets a custom type for stack index ]")
    

def main():
    help_flag=False
    source = None
    includes = []
    out_file = "out.c"
    debug=False
    alone=False
    table_max="32"
    index_type="uint32_t"
    stack_max="256"
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
                continue
        elif arg=="--stack-max":
            arg_index+=1
            stack_max=sys.argv[arg_index]
            continue
        elif arg=="--index-type":
            arg_index+=1
            index_type=sys.argv[arg_index]
            continue
        elif arg=="--table-max":
            arg_index+=1
            table_max=sys.argv[arg_index]
            continue
        elif arg=="-v":
            debug=True
        arg_index+=1
    if help_flag:
        cynk_help()
    elif source is not None:
        config["output_filename"] = out_file
        config["stack_max"] = stack_max
        config["index_type"] = index_type
        config["table_cap"] = table_max
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


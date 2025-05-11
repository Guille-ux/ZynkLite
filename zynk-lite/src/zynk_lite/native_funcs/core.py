# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# clase core de las funciones nativas y alguna que otra función

import time
import random
import os


class ZynkNativeFunc: #emulador de funciones
    def __init__(self, func):
        self.func = func
    def call(self, interpreter, args):
        return self.func(args)
    def __repr__(self):
        return f"<native fn>"

#tiempo

def clock(args):
    return time.time()
def slep(args):
    time.sleep(args[0])
    return None

#random
def choic(args):
    return random.choice(args[0])
def randi(args):
    return random.randint(min(int(args[0]), int(args[1])), max(int(args[0]), int(args[1])))
def randf(args):
    return random.uniform(min(args[0], args[1]), max(args[0], args[1]))
def rand(args):
    return random.random()
#arrays

def lenght(args):
    return len(args[0])
def get_index(args):
    return args[0][int(args[1])]
def set_index(args):
    args[0][int(args[1])]=args[2]
    return None
def push(args):
    args[0].append(args[1])
    return None
def pup(args):
    args[0].pop(int(args[1]))
    return None

#FUNCIONES DE IO y otras cosas, hay que recordar que esto son modulos al fin de al cabo
#el interprete de C no tendra todas estas, tendra otras
#jijijiji, ya me pondre a hacer el bytecode
#

#
#  args[0] es el nombre
# cuando sea necesario args[1] es la información

def write_file(args):
    name = args[0]
    data = args[1]
    with open(name, "w") as f:
        f.write(data)
    return None
def read_file(args):
    name = args[0]
    with open(name, "r") as f:
        data = f.read()
    return data
def write_bytes(args):
    name = args[0]
    data = args[1]
    with open(name, "wb") as f:
        f.write(data)
    return None
def read_bytes(args):
    name = args[0]
    with open(name, "rb") as f:
        data = f.read()
    return data
def makedir(args):
    os.makedirs(args[0])
    return None
def listdir(args):
    return os.listdir()
def pwd(args):
    return os.getcwd()
def cwd(args):
    os.chdir(args[0])
    return None
def rmdir(args):
    os.removedirs(args[0])
    return None
def remove(args):
    os.remove(args[0])
    return None


# float a str y viceversa
def tfloat(args):
    return float(args[0])
def tstr(args):
    return str(args[0])
def tint(args):
    return int(args[0])

# input y print
def nprint(args):
    print(args[0])
    return None
def ninput(args):
    return input(args[0])

# time
nclock = ZynkNativeFunc(clock)
nsleep = ZynkNativeFunc(slep)

# arrays
nlenght = ZynkNativeFunc(lenght)
nget_index = ZynkNativeFunc(get_index)
nset_index = ZynkNativeFunc(set_index)
npush = ZynkNativeFunc(push)
npop = ZynkNativeFunc(pup)

#archivos
nwf = ZynkNativeFunc(write_file)
nrf = ZynkNativeFunc(read_file)
nwb = ZynkNativeFunc(write_bytes)
nrb = ZynkNativeFunc(read_bytes)

# conversion

ntf = ZynkNativeFunc(tfloat)
nts = ZynkNativeFunc(tstr)
nti = ZynkNativeFunc(tint)

#números aleatorios

nchoice = ZynkNativeFunc(choic)
nrandint = ZynkNativeFunc(randi)
nrandf = ZynkNativeFunc(randf)
nrandom = ZynkNativeFunc(rand)


#other filesystem interactions
nmakedir = ZynkNativeFunc(makedir)
nlistdir = ZynkNativeFunc(listdir)
npwd = ZynkNativeFunc(pwd)
ncwd = ZynkNativeFunc(cwd)
nrmdir = ZynkNativeFunc(rmdir)
nremove = ZynkNativeFunc(remove)

# input and print
ninp = ZynkNativeFunc(ninput)
npri = ZynkNativeFunc(nprint)

def add_natives(eval, funcs):
    for k, v in funcs.items():
        eval.env.define(k, v)


# CORE FUNCS
core_funcs = {
    "clock":nclock,
    "len":nlenght,
    "get_index":nget_index,
    "set_index":nset_index,
    "push":npush,
    "write":nwf,
    "read":nrf,
    "write_bytes":nwb,
    "read_bytes":nrb,
    "str":nts,
    "float":ntf,
    "int":nti,
    "pop":npop,
    "sleep":nsleep,
    "choice":nchoice,
    "randi":nrandint,
    "randf":nrandf,
    "rand":nrandom,
    "mkdir":nmakedir,
    "listdir":nlistdir,
    "pwd":npwd,
    "cwd":ncwd,
    "rmdir":nrmdir,
    "remove":nremove,
    "print":npri,
    "input":ninp
}
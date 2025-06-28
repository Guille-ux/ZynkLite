# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

cynk_headers_defaults = {
            "cynk_header_names":["cynk_stack.h", "cynk_memory.h", "cynk_env.h"],
        }

stack_defaults = {
            "index_type":"uint32_t",
            "stack_max":"256"
        }

stack_headers = """ 
#ifndef CYNK_STACK
#define CYNK_STACK

#include "libzynk/zynk.h"
#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

#define STACK_MAX {stack_max}

{index_type} index=0;

Value stack[STACK_MAX];

Value cynkPop();

void cynkPush(Value val);

void cynkSwap();

Value cynkPop() {{
    if (index == 0) return zynkNull();
    index--;
    return stack[index];
}}

void cynkDel() {{
	if (index==STACK_MAX) return;
	zynk_release(stack[index+1], &sysarena);
}}

void cynkPush(Value val) {{
    if (index==STACK_MAX) return;
    if (stack[index]!=val) {{
        zynk_release(stack[index], &sysarena);
    }}
    stack[index++] = val;
}}

void cynkSwap() {{
    if (index<2) return;
    Value __a__=cynkPop();
    Value __b__=cynkPop();
    cynkPush(__a__);
    cynkPush(__b__);
}}

"""

sysarena_defaults = {
            "num_arenas":"2048",
            "memory_size":"1024*1024",
            "a_or_b":"ANSI",
        }
sysarena_header = """

#ifndef CYNK_SYSARENA_SETUP
#define CYNK_SYSARENA_SETUP

#include "libzynk/zynk.h"
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#define NUM_ARENAS {num_arenas}
#define MEM_SIZE {memory_size}
#define {a_or_b} // STANDALONE or ANSI?

ArenaManager sysarena;

bool cynkSysarenaInit();

#ifdef STANDALONE
Arena arena_pool[NUM_ARENAS];
uint8_t memory_pool[MEM_SIZE];

bool cynkSysarenaInit() {{
    return sysarena_init(&sysarena, memory_pool, arena_pool, MEM_SIZE, NUM_ARENAS);
}}
#endif


#ifdef ANSI
#include <stdlib.h>
#include <stdio.h>
Arena *arena_pool;
uint8_t *memory_pool;

bool cynkSysarenaInit() {{
    arena_pool = (Arena *)malloc(sizeof(Arena)*NUM_ARENAS);
    memory_pool = (uint8_t *)malloc(MEM_SIZE);
    if (arena_pool==NULL || memory_pool==NULL) return false;
    return sysarena_init(&sysarena, memory_pool, arena_pool, MEM_SIZE, NUM_ARENAS);
}}
#endif

#endif

"""

zenv_defaults = {
            "table_cap":"32",
        }

zenv_headers = """

#ifndef CYNK_ENV
#define CYNK_ENV

#include "libzynk/zynk.h"
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#define CYNK_ENV_CAP {table_cap}

// ahora vienen los helpers, porque crear entornos es una pesadilla, xD

ZynkEnv* cynkEnvCreate(ZynkEnv *enclosing, size_t capacity, ArenaManager *manager);
bool cynkFreeEnv(ZynkEnv *env, ArenaManager *manager);
ZynkEnv* cynkEnvBack(ZynkEnv *env, ArenaManager *manager);




// Implementaciones!

ZynkEnv* cynkEnvCreate(ZynkEnv *enclosing, size_t capacity, ArenaManager *manager) {{
    ZynkEnv *new_env = (ZynkEnv *)sysarena_alloc(manager, sizeof(ZynkEnv));
    if (new_env==NULL) return NULL;

    new_env->local = (ZynkEnvTable *)sysarena_alloc(manager, sizeof(ZynkEnvTable));// asignar tabla local
    if (new_env->local == NULL) {{
        sysarena_free(manager, new_env);
        return NULL;
    }}
    new_env->local->entries = (ZynkEnvEntry**)sysarena_alloc(manager, sizeof(ZynkEnvEntry*)*capacity);
    if (new_env->local->entries==NULL) {{
        sysarena_free(manager, new_env->local);
        sysarena_free(manager, new_env);
        return NULL;
    }}
    
    if (!zynkEnvInit(new_env, capacity, enclosing, manager)) {{
        sysarena_free(manager, new_env->local->entries);
        sysarena_free(manager, new_env->local);
        sysarena_free(manager, new_env);
        return NULL;
    }}
    return new_env;
}}

bool cynkFreeEnv(ZynkEnv *env, ArenaManager *manager) {{
    if (env==NULL || manager==NULL) return false;

    bool success=true;
    
    if (env->local!=NULL) {{
        for (size_t i=0;i<env->local->capacity;i++) {{
            if (env->local->entries[i]!=NULL && env->local->entries[i]->name!=NULL) zynk_release(env->local->entries[i]->value, manager);
        if (!freeZynkTable(manager, env->local)) success=false;
        }}
    }}

    if (!sysarena_free(manager, env)) success=false;

    return success;
}}

ZynkEnv* cynkEnvBack(ZynkEnv *env, ArenaManager *manager) {{
    if (env==NULL || env->enclosing==NULL) return NULL;

    ZynkEnv *__tmp__=env;
    env=__tmp__->enclosing;
    if (!cynkFreeEnv(__tmp__, manager)) return NULL;

    return env;
}}

#endif

"""

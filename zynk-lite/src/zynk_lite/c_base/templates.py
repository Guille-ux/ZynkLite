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
	zynk_release(stack[index+1]);
}}

void cynkPush(Value val) {{
    if (index==STACK_MAX) return;
    if (stack[index]!=val) {{
        zynk_release(stack[index]);
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

ZynkEnv* cynkEnvCreate(ZynkEnv *enclosing, size_t capacity);
bool cynkFreeEnv(ZynkEnv *env);
ZynkEnv* cynkEnvBack(ZynkEnv *env);




// Implementaciones!

ZynkEnv* cynkEnvCreate(ZynkEnv *enclosing, size_t capacity) {{
    ZynkEnv *new_env = (ZynkEnv *)malloc(sizeof(ZynkEnv));
    if (new_env==NULL) return NULL;

    new_env->local = (ZynkEnvTable *)malloc(sizeof(ZynkEnvTable));// asignar tabla local
    if (new_env->local == NULL) {{
        free(new_env);
        return NULL;
    }}
    new_env->local->entries = (ZynkEnvEntry**)malloc(sizeof(ZynkEnvEntry*)*capacity);
    if (new_env->local->entries==NULL) {{
        free(new_env->local);
        free(new_env);
        return NULL;
    }}
    
    if (!zynkEnvInit(new_env, capacity, enclosing)) {{
        free(new_env->local->entries);
        free(new_env->local);
        free(new_env);
        return NULL;
    }}
    return new_env;
}}

bool cynkFreeEnv(ZynkEnv *env) {{
    if (env==NULL) return false;

    bool success=true;
    
    if (env->local!=NULL) {{
        for (size_t i=0;i<env->local->capacity;i++) {{
            if (env->local->entries[i]!=NULL && env->local->entries[i]->name!=NULL) zynk_release(env->local->entries[i]->value);
        if (!freeZynkTable(env->local)) success=false;
        }}
    }}

    if (!free(env)) success=false;

    return success;
}}

ZynkEnv* cynkEnvBack(ZynkEnv *env) {{
    if (env==NULL || env->enclosing==NULL) return NULL;

    ZynkEnv *__tmp__=env;
    env=__tmp__->enclosing;
    if (!cynkFreeEnv(__tmp__)) return NULL;

    return env;
}}

#endif

"""

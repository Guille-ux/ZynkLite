 
#ifndef CYNK_STACK
#define CYNK_STACK

#include "libzynk/zynk.h"
#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

#define STACK_MAX 256

uint32_t index=0;

Value stack[STACK_MAX];

Value cynkPop();

void cynkPush(Value val);

void cynkSwap();

Value cynkPop() {
    if (index == 0) return zynkNull();
    index--;
    return stack[index];
}

void cynkDel() {
	if (index==STACK_MAX) return;
	zynk_release(stack[index+1], &sysarena);
}

void cynkPush(Value val) {
    if (index==STACK_MAX) return;
    if (stack[index]!=val) {
        zynk_release(stack[index], &sysarena);
    }
    stack[index++] = val;
}

void cynkSwap() {
    if (index<2) return;
    Value __a__=cynkPop();
    Value __b__=cynkPop();
    cynkPush(__a__);
    cynkPush(__b__);
}




#ifndef CYNK_SYSARENA_SETUP
#define CYNK_SYSARENA_SETUP

#include "libzynk/zynk.h"
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#define NUM_ARENAS 2048
#define MEM_SIZE 1024*1024
#define ANSI // STANDALONE or ANSI?

ArenaManager sysarena;

bool cynkSysarenaInit();

#ifdef STANDALONE
Arena arena_pool[NUM_ARENAS];
uint8_t memory_pool[MEM_SIZE];

bool cynkSysarenaInit() {
    return sysarena_init(&sysarena, memory_pool, arena_pool, MEM_SIZE, NUM_ARENAS);
}
#endif


#ifdef ANSI
#include <stdlib.h>
#include <stdio.h>
Arena *arena_pool;
uint8_t *memory_pool;

bool cynkSysarenaInit() {
    arena_pool = (Arena *)malloc(sizeof(Arena)*NUM_ARENAS);
    memory_pool = (uint8_t *)malloc(MEM_SIZE);
    if (arena_pool==NULL || memory_pool==NULL) return false;
    return sysarena_init(&sysarena, memory_pool, arena_pool, MEM_SIZE, NUM_ARENAS);
}
#endif

#endif




#ifndef CYNK_ENV
#define CYNK_ENV

#include "libzynk/zynk.h"
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#define CYNK_ENV_CAP 32

// ahora vienen los helpers, porque crear entornos es una pesadilla, xD

ZynkEnv* cynkEnvCreate(ZynkEnv *enclosing, size_t capacity, ArenaManager *manager);
bool cynkFreeEnv(ZynkEnv *env, ArenaManager *manager);
ZynkEnv* cynkEnvBack(ZynkEnv *env, ArenaManager *manager);




// Implementaciones!

ZynkEnv* cynkEnvCreate(ZynkEnv *enclosing, size_t capacity, ArenaManager *manager) {
    ZynkEnv *new_env = (ZynkEnv *)sysarena_alloc(manager, sizeof(ZynkEnv));
    if (new_env==NULL) return NULL;

    new_env->local = (ZynkEnvTable *)sysarena_alloc(manager, sizeof(ZynkEnvTable));// asignar tabla local
    if (new_env->local == NULL) {
        sysarena_free(manager, new_env);
        return NULL;
    }
    new_env->local->entries = (ZynkEnvEntry**)sysarena_alloc(manager, sizeof(ZynkEnvEntry*)*capacity);
    if (new_env->local->entries==NULL) {
        sysarena_free(manager, new_env->local);
        sysarena_free(manager, new_env);
        return NULL;
    }
    
    if (!zynkEnvInit(new_env, capacity, enclosing, manager)) {
        sysarena_free(manager, new_env->local->entries);
        sysarena_free(manager, new_env->local);
        sysarena_free(manager, new_env);
        return NULL;
    }
    return new_env;
}

bool cynkFreeEnv(ZynkEnv *env, ArenaManager *manager) {
    if (env==NULL || manager==NULL) return false;

    bool success=true;
    
    if (env->local!=NULL) {
        for (size_t i=0;i<env->local->capacity;i++) {
            if (env->local->entries[i]!=NULL && env->local->entries[i]->name!=NULL) zynk_release(env->local->entries[i]->value, manager);
        if (!freeZynkTable(manager, env->local)) success=false;
        }
    }

    if (!sysarena_free(manager, env)) success=false;

    return success;
}

ZynkEnv* cynkEnvBack(ZynkEnv *env, ArenaManager *manager) {
    if (env==NULL || env->enclosing==NULL) return NULL;

    ZynkEnv *__tmp__=env;
    env=__tmp__->enclosing;
    if (!cynkFreeEnv(__tmp__, manager)) return NULL;

    return env;
}

#endif



// Zynk Function Declarations


        // Headers Generated with InitProgram class from zynk_lite/c_base/initialize.py

        

// C Main Function and Zynk Entry Point


int main() {
    if (!cynkSysarenaInit()) {
        return 1;
    }
    
    ZynkEnv *env = cynkEnvCreate(NULL, CYNK_ENV_CAP, &sysarena); 
    if (env == NULL) {
        return 1;
    }
    
    // Código Zynk de nivel superior transpiled
    env = cynkEnvCreate(env, CYNK_ENV_CAP, &sysarena);
{
Value __tmp__=zynkCreateArray(&sysarena, 1);
cynkPush(zynkCreateString(&sysarena, "Hola!"));
zynkArrayPush(&sysarena, __tmp__, cynkPop());
cynkPush(zynkCallFunction(&sysarena, env, "print", __tmp__));
}
env = cynkEnvBack(env, &sysarena);


    cynkFreeEnv(env, &sysarena); 
    
    return 0;
}


// Zynk Function Implementations

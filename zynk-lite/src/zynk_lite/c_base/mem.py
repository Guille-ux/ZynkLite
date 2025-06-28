# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

from . import templates

class MemoryManager:
    def emit_nenv(self):
        return 'env = cynkEnvCreate(env, CYNK_ENV_CAP, &sysarena);'
    def emit_ret_env(self):
        return 'env = cynkEnvBack(env, &sysarena);'
    def emit_set(self, name, stack):
        return f'zynkTableSet(&sysarena, env, "{name}", {stack.spop()});'
    def emit_new(self, name, stack):
        return f'zynkTableNew(env, "{name}", {stack.spop()}, &sysarena);'
    def emit_get(self, name):
        return f'zynkTableGet(env, "{name}")'
    def emit_pget(self, name, stack):
        return stack.spush(self.emit_get(name))

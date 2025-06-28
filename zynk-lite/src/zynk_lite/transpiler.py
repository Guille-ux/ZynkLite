# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

from .c_base import templates, stack, mem, initialize, funcs 
from .c_base.translator import Cynk 
from .frontend.lexer import ZynkLLexer 
from .ast.parser import ZynkLParser    
from .ast import expressions as zexpr 
from . import tokens 
from . import errors

class Transpiler:
    def __init__(self, config=None, debug=False):
        self.debug=debug
        self.config = {
            "stack_max": templates.stack_defaults["stack_max"],
            "index_type": templates.stack_defaults["index_type"],
            "num_arenas": templates.sysarena_defaults["num_arenas"],
            "memory_size": templates.sysarena_defaults["memory_size"],
            "a_or_b": templates.sysarena_defaults["a_or_b"], # "ANSI" o "STANDALONE"
            "table_cap": templates.zenv_defaults["table_cap"],
            "output_filename": "output.c",
            "main_function_name": "main",
            "prefix": "zynk_func", 
        }
        if config:
            self.config.update(config)

        # Inicializa las herramientas del compilador
        self.lexer = ZynkLLexer(None, debug=True)
        self.parser = ZynkLParser(None, debug=True)
        
        self.cynk_translator = Cynk(
            debug=False
        )

        self.cynk_translator.prefix = self.config["prefix"] 
        self.main_program_c_code = ""
        self.defines = {} # Para el preprocesador simple

    def _simple_preprocess(self, source_code):
        lines = source_code.splitlines()
        processed_lines = []
        if_stack = [] 

        for line in lines:
            stripped_line = line.strip()

            if stripped_line.startswith("#define "):
                parts = stripped_line.split(maxsplit=2)
                if len(parts) >= 2:
                    key = parts[1]
                    value = parts[2] if len(parts) == 3 else ""
                    self.defines[key] = value
                continue 

            elif stripped_line.startswith("#ifdef "):
                macro = stripped_line.split(maxsplit=1)[1].strip()
                condition_met = macro in self.defines
                if_stack.append(condition_met)
                continue

            elif stripped_line.startswith("#ifndef "):
                macro = stripped_line.split(maxsplit=1)[1].strip()
                condition_met = macro not in self.defines
                if_stack.append(condition_met)
                continue

            elif stripped_line.startswith("#endif"):
                if if_stack:
                    if_stack.pop()
                continue
            
            if all(if_stack):
                processed_lines.append(line)
        
        return "\n".join(processed_lines)

    def transpile(self, src, includes=[]):
        zynk_source_code = ""
        for include in includes:
            with open(include, "r") as f:
                included = f.read()
            zynk_source_code += included + "\n"
        zynk_source_code += src
        processed_zynk_code = self._simple_preprocess(zynk_source_code)
        
        self.lexer.source = processed_zynk_code
        tokens_list = self.lexer.scan()
        if self.debug:
            for token in tokens_list:
                print(f"[ + {token} + ]")
        self.parser.tokens = tokens_list
        ast_root_statements = self.parser.parse()

        if self.debug:
            print(f"[ AST : {ast_root_statements} ]")
        self.cynk_translator.context = "" 
        self.cynk_translator.visit_block(ast_root_statements, origin=False)
        self.main_program_c_code = self.cynk_translator.pop_ctx()

        final_c_output_parts = []

        final_c_output_parts.append(templates.stack_headers.format(
            stack_max=self.config["stack_max"],
            index_type=self.config["index_type"]
        ))
        final_c_output_parts.append(templates.sysarena_header.format(
            num_arenas=self.config["num_arenas"],
            memory_size=self.config["memory_size"],
            a_or_b=self.config["a_or_b"]
        ))
        final_c_output_parts.append(templates.zenv_headers.format(
            table_cap=self.config["table_cap"],
            cynk_header_names=templates.cynk_headers_defaults["cynk_header_names"]
        ))

        final_c_output_parts.append("\n// Zynk Function Declarations\n")
        final_c_output_parts.append(self.cynk_translator.program_header.emit())

        final_c_output_parts.append("\n// C Main Function and Zynk Entry Point\n")
        final_c_output_parts.append(f"""
int {self.config["main_function_name"]}() {{
    if (!cynkSysarenaInit()) {{
        return 1;
    }}
    
    ZynkEnv *env = cynkEnvCreate(NULL, CYNK_ENV_CAP, &sysarena); 
    if (env == NULL) {{
        return 1;
    }}
    
    // Código Zynk de nivel superior transpiled
    {self.main_program_c_code}

    cynkFreeEnv(env, &sysarena); 
    
    return 0;
}}
""")

        # Implementaciones de funciones Zynk
        final_c_output_parts.append("\n// Zynk Function Implementations\n")
        for func_c_code_block in self.cynk_translator.code:
             final_c_output_parts.append(func_c_code_block)
             final_c_output_parts.append("\n")

        return "\n".join(final_c_output_parts)

    def write_output(self, c_code_content):
        output_filepath = self.config["output_filename"]
        try:
            with open(output_filepath, "w") as f_out:
                f_out.write(c_code_content)
            print(f"C Code generated at '{output_filepath}'")
        except IOError as e:
            print(f"Error writing '{output_filepath}': {e}")


# --- Ejemplo de uso del Transpilador ---
if __name__ == "__main__":
    zynk_test_code = """
call print("Hola!");
"""

    my_transpiler = Transpiler(config={
        "output_filename": "final_program.c",
        "a_or_b": "ANSI", 
    }, debug=True)

    try:
        final_c_code = my_transpiler.transpile(zynk_test_code)
        my_transpiler.write_output(final_c_code)
    except Exception:
        print("[ Error ]")

from .ast import parser, expressions, eval, zenv
from .frontend import lexer
from .c_base import translator, initialize
from . import tokens, errors

test_expr_src = [
        "2 + 3",
        "5*2",
        "7-1",
        "5*3-1",
        "4+2*2-1+3",
        "4*2/3-1",
        "5*2-1/3*2",
        "7/2+0.5-1",
        "7 == 7",
        "5 - 3 > 5",
        "2 - 4 < 3",
        "2 < 3 and 5 > 3",
        "2 - 1 > 2 or 5 - 1 < 10",
        ]

if __name__ == "__main__":
    print("[+] Testing Mathematical Expressions [+]")
    for test in test_expr_src:
        print(f"[+] Expr : {test} [+]")
        zlexer = lexer.ZynkLLexer(test, debug=True)
        print("[+] Lexing... [+]")
        tokens = zlexer.scan()
        zparser = parser.AlgebraicParser(tokens, debug=True)
        print("[+] Lexing Process Finished [+]")
        for token in tokens:
            print(f"[+] : {token} : [+]")
        print("[+] Parsing... [+]")
        test_ast = zparser.parse()
        print("[+] Parsing Process Finished [+]")
        print(f"[+] AST (Abstract Syntax Tree) : {test_ast} [+]")
        print("[+] Transpiling to C... [+]")
        ztrans = translator.Cynk()
        ztrans.eval(test_ast)
        print("[+] Code Transpiled! [+]")
        print("[+] Current Context [+]")
        print(ztrans.context)
        print("[+] Final C Code [+]")
        print("\n".join(ztrans.code))

# Zynk Lite Docs
The docs are first at the wiki **:)**, please visit it.

# Syntax
### Tokens
*```ZynkLite```* has **45** tokens.
-----------------
*TokenType Class*
```python
# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

class TokenType:
    #delimitadores
    LPAREN = 0 # (
    RPAREN = 1 # )
    LBRACE = 2 # {
    RBRACE = 3 # }
    LBRACKET = 4 # [
    RBRACKET = 5 # ] 
    COMMA = 6 # ,
    SEMICOLON = 7 # ;
    DOT = 8 # .
    COLON = 9 # :
    EQUAL = 21 # =

    # Tipos de Datos
    FLOAT = 10 # números de punto flotante
    ARRAY = 11 # una lista bro, como los hare???
        # STRUCTS ¿?
    STRING = 12
    NULL = 13
    BOOL = 14

    # Aritmetica/Lógica

    STAR = 15 # *
    SLASH = 16 # /
    MINUS = 17
    PLUS = 18
    GREATER = 19
    LESS = 20
    EQUAL_EQUAL = 22 # ==
    LESS_EQUAL = 23 # <=
    GREATER_EQUAL = 24 # >=
    BANG = 25 # !
    BANG_EQUAL = 26 # !=
    AND = 27
    OR = 28
    XOR = 29

    # Abstracto
    IDENTIFIER = 30

    # Palabras Clave

    VAR = 31
    LIST = 32
    FUNC = 33
    CALL = 34
    TO = 35
    AS = 45
    RETURN = 36
    ELSE = 37
    IF = 38
    WHILE = 39
    FOR = 40

    # built-in
    INPUT = 41
    PRINT = 42
    IMPORT = 43
    
    # IDK
    EOF = 44
```
*Note: the token list isn't used in the language*

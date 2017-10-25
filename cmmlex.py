import ply.lex as lex
from types import Node,BinOp

# List of keywords
keywords = {
        'if'     : 'IF',
        'else'   : 'ELSE',
        'while'  : 'WHILE',
        'for'    : 'FOR',
        'return' : 'RETURN',
        'extern' : 'EXTERN',
        'void'   : 'VOID',
        'char'   : 'CHAR',
        'int'    : 'INT',
}

# List of tokens
tokens = [
        'INTCON',
        'ID',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'LPAREN',
        'RPAREN',
        'LCURLY',
        'RCURLY',
        'LSQUARE',
        'RSQUARE',
        'COMMA',
        'SEMICOLON',
        'EQUAL',
        'NOT',
        'NOTEQUAL',
        'LESSEQUAL',
        'LESS',
        'MOREEQUAL',
        'MORE',
        'AND',
        'OR',
        'COMMENT',
        'CHARCON',
        'STRINGCON',
        'ASSIGNMENT'
] + list(keywords.values())

# Regex for simpler tokens
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LCURLY    = r'\{'
t_RCURLY    = r'\}'
t_LSQUARE   = r'\['
t_RSQUARE   = r'\]'
t_COMMA     = r'\,'
t_SEMICOLON = r';'
t_EQUAL     = r'=='
t_NOT       = r'\!'
t_NOTEQUAL  = r'\!='
t_LESSEQUAL = r'<='
t_LESS      = r'<'
t_MOREEQUAL = r'>='
t_MORE      = r'>'
t_AND       = r'&&'
t_OR        = r'\|\|'
t_COMMENT   = r'\/\*(\w|\W)*\*\/'
t_CHARCON   = r'\'([ -~] | \n | \0)\''
t_STRINGCON = r'\"([ -~] | \0)*\"'
t_ASSIGNMENT = r'='

# More specefic regex
def t_INTCON(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = keywords.get(t.value, 'ID')
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


#### Build the lexer
lexer = lex.lex()
# Give the lexer some input
with open ("test.c", "r") as myfile:
    data=myfile.read()
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)

# Start the parsing
import ply.yacc as yacc

def p_prog_dcl(p):
    '''prog : dcl SEMICOLON prog
            | dcl SEMICOLON empty'''
    p[0] = Prog('prog', [p[1], p[3]], None)
def p_prog_func(p):
    '''prog : dcl func prog
            | dcl func empty'''
    p[0] = Prog('prog', [p[1]], None)

def p_dcl(p):
    pass

def p_var_decl(p):
    pass

def p_typy(p):
    pass

def p_param_types(p):
    pass

def p_func(p):
    pass

def p_stmt(p):
    pass

def p_assg(p):
    pass

def p_expr(p):
    pass

def p_binop(p):
    '''binop : PLUS
             | MINUS
             | TIMES
             | DIVIDE'''
    p[0] = BinOp('binop', None, p[1])

def p_relop(p):
    '''relop : EQUAL
             | NOTEQUAL
             | LESSEQUAL
             | LESS
             | MOREEQUAL
             | MORE'''
    p[0] = RelOp('relop', None, p[1])

def p_logical_op(p):
    '''logical_op : AND
                  | OR'''
    p[0] = LogicalOp('logical_op', None, p[1])

def p_empty(p):
    '''empty :'''
    pass

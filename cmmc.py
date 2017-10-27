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
    '''prog : prog dcl SEMICOLON
            | prog func
            |'''
    p[0] = Prog('prog', [p[1], p[2]], None)


def p_dcl_first(p): # dcl : type var_decl dcl_prime
    '''dcl : type var_decl decl_p
           | dcl_extern VOID ID LPAREN param_types RPAREN dcp_pp
           | dcl_extern type ID LPAREN param_types RPAREN dcp_pp'''
    if(len(p) > 4):
        p[0] = Dcl('dcl', [(p[4], p[3], p[6] ), *p[8]] ,p[1])
    else
        p[0] = Dcl('dcl', [ p[1], [p[2], *p[3]] ], None)
def p_dcl_p(p):
    '''dcl_p : COMMA var_decl dcl_p
             |'''
    if(len(p[0]) > 1):
        p[0] = [p[2], *p[3]]
    else:
        pass
def p_dcl_pp(p):
    ''' dcl_pp : COMMA ID LPAREN param_types RPAREN dcl_pp
               |'''
    if(len(p[0]) > 1):
        p[0] = [(p[2], p[4]), *p[6]]
    else:
        pass


def p_var_decl(p):
    '''var_decl : ID
                | ID LSQUARE INTCONT RSQUARE'''
    p[0] = VarDecl('var_decl', None, p[1])
    if(len(p) > 2):
        p[0].num_elements = int(p[3])

def p_typy(p):
    '''type : CHARCON
            | INTCON'''
    p[0] = Type('type', None, p[1])

def p_param_types(p):
    '''param_types : VOID
                   | type ID param_types_array param_types_more'''
    if(len(p) > 2):
        p[0] = ParamTypes('param_types', [(p[2], p[1], p[3]), *p[4]])
    else:
        p[0] = ParamTypes('param_types', None, p[1])
def p_param_types_array(p):
    '''param_types_array : LPAREN RPAREN
                         |'''
    if(len(p) > 2):
        p[0] = "array"
    else:
        p[0] = None
def p_param_types_more(p):
    '''param_types_more : COMMA type ID param_types_array param_types_more
                        |'''
    p[0] = [(p[4], p[3], p[5]), *p[6]]

def p_func(p):
    pass

def p_stmt_if(p):
    '''stmt : IF LPAREN expr RPAREN stmt stmt_else'''
    pass #TODO
def p_stmt_else(p):
    '''stmt_else : ELSE stmt
                 |'''
    pass #TODO
def p_stmt_while(p):
    '''stmt : WHILE LPAREN expr RPAREN stmt'''
    pass #TODO
def p_stmt_for(p):
    '''stmt : FOR LPAREN stmt_opt_assg SEMICOLON stmt_opt_expr SEMICOLON stmt_opt_assg RPAREN stmt'''
    pass #TODO
def p_stmt_opt_assg(p):
    '''stmt_opt_assg : assg
                     |'''
    pass #TODO
def p_stmt_opt_expr(p):
    '''stmt_opt_expr : expr
                     |'''
    pass #TODO
def p_stmt_return(p):
    '''stmt : RETURN stmt_opt_expr SEMICOLON'''
    pass #TODO
def p_stmt_assg(p):
    '''stmt : assg SEMICOLON'''
    pass #TODO
def p_stmt_id(p):
    '''stmt : ID LPAREN expr_pp RPAREN SEMICOLON'''
    pass #TODO
def p_stmt_enclose(p):
    '''stmt : LCURLY stmt_repeat RCURLY'''
    pass #TODO
def p_stmt_repeat(p):
    '''stmt_repeat : stmt stmt_repeat
                   |'''
    pass #TODO
def p_stmt_end(p):
    '''stmt : SEMICOLON'''
    pass #TODO

def p_assg(p):
    '''assg : ID assg_p ASSIGNMENT expr'''
    p[0] = Assg('Assg', p[4], (p[1], p[2]) )
def p_assg_p(p):
    '''assg : LSQUARE expr RSQUARE
            |'''
    if(len(p) > 2):
        p[0] = p[2]
    else:
        p[0] = None

def p_expr_single(p):
    '''expr : MINUS expr
            | NOT expr'''
    p[0] = Expr('expr', p[2], p[1])
def p_expr_multi(p):
    '''expr : expr binop expr
            | expr relop expr
            | expr logical_op expr'''
    p[0] = Expr('expr', [p[1], p[3]], p[2])
def p_expr_terminals(p):
    '''expr : INTCON
            | CHARCON
            | STRINGCON'''
    p[0] = Expr('expr', None, p[1])
def p_expr_sub(p):
    '''expr : LPAREN expr RPAREN'''
    p[0] = p[2]
def p_expr_id(p):
    '''expr : ID expr_p'''
    p[0] = Expr('expr', p[2], p[1])
def p_expr_p(p):
    '''expr_p : LPAREN expr_pp RPAREN
              | LSQUARE expr RSQUARE'''
    p[0] = p[2]
def p_expr_pp(p):
    '''expr_pp : expr expr_ppp
               |'''
    p[0] = [p[1], *p[2]]
def p_expr_p(p):
    '''expr_ppp : COMMA expr expr_ppp
                | '''
    p[0] = [p[2], *p[3]]

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

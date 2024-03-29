#!/usr/bin/env python3
import ply.lex as lex
from parser_types import *
import sys

if len(sys.argv) < 2:
    print("Usage: %s [c source file]" % sys.argv[0])
    exit(1)

VERBOSE = False

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
        'float'  : 'FLOAT',
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
        'CHARCON',
        'STRINGCON',
        'FLOATCON',
        'ASSIGNMENT',
] + list(keywords.values())

# Regex for simpler tokens
t_PLUS       = r'\+'
t_MINUS      = r'-'
t_TIMES      = r'\*'
t_DIVIDE     = r'/'
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_LCURLY     = r'\{'
t_RCURLY     = r'\}'
t_LSQUARE    = r'\['
t_RSQUARE    = r'\]'
t_COMMA      = r'\,'
t_SEMICOLON  = r';'
t_EQUAL      = r'== '
t_NOT        = r'\!'
t_NOTEQUAL   = r'\!='
t_LESSEQUAL  = r'<= '
t_LESS       = r'<'
t_MOREEQUAL  = r'>='
t_MORE       = r'>'
t_AND        = r'&&'
t_OR         = r'\|\|'
t_CHARCON    = r'\'([ -~] | \n | \0)\''
t_STRINGCON  = r'\"([ -~] | \0)*\"'
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

def t_FLOATCON(t):
    r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
    t.value = float(t.value)

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_comment(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    t.lineno += t.value.count('\n')

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


#### Build the lexer
lexer = lex.lex()
# Give the lexer some input
with open (sys.argv[1], "r") as myfile:
    data=myfile.read()

# Start the parsing
import ply.yacc as yacc

# prog : { dcl ';'  |  func }
def p_prog(p):
    '''prog : prog dcl SEMICOLON
            | prog func
            |'''
    if(len(p) > 1):
        if(p[1] != None):
            p[0] = [*p[1], p[2]]
        else:
            p[0] = [p[2]]
    else:
        p[0] = None

# dcl : type var_decl { ',' var_decl }
#     | [ extern ] type id '(' param_typesm_types ')' { ',' id '(' parm_types ')' }
#     | [ extern ] void id '(' param_typesm_types ')' { ',' id '(' parm_types ')' }
def p_dcl_first(p): # dcl : type var_decl dcl_prime
    '''dcl : CHAR var_decl dcl_p
           | INT var_decl dcl_p
           | FLOAT var_decl dcl_p
           | CHAR ID LPAREN param_types RPAREN dcl_p
           | INT ID LPAREN param_types RPAREN dcl_p
           | FLOAT ID LPAREN param_types RPAREN dcl_p
           | VOID ID LPAREN param_types RPAREN dcl_p
           | EXTERN CHAR ID LPAREN param_types RPAREN dcl_p
           | EXTERN INT ID LPAREN param_types RPAREN dcl_p
           | EXTERN FLOAT ID LPAREN param_types RPAREN dcl_p
           | EXTERN VOID ID LPAREN param_types RPAREN dcl_p'''
    if(len(p) > 6):
        if(p[7] != None):
            p[0] = Dcl('dcl-func-extern', [(p[3], p[5]), *p[7]], p[2],
                    p.lexer.lineno)
        else:
            p[0] = Dcl('dcl-func-extern', [(p[3], p[5])], p[2], p.lexer.lineno)
    elif(len(p) > 4):
        if(p[6] != None):
            p[0] = Dcl('dcl-func', [(p[2], p[4]), *p[6]] ,p[1], p.lexer.lineno)
        else:
            p[0] = Dcl('dcl-func', [(p[2], p[4])] ,p[1], p.lexer.lineno)
    else:
        if(p[3] != None):
            p[0] = Dcl('dcl-var', [ p[2], *p[3] ], p[1], p.lexer.lineno)
        else:
            p[0] = Dcl('dcl-var', [ p[2] ], p[1], p.lexer.lineno)
def p_dcl_p(p):
    '''dcl_p : COMMA var_decl dcl_pp
             |'''
    if(p != None and len(p) > 1):
        if(p[3] != None):
            p[0] = [p[2], *p[3]]
        else:
            p[0] = [p[2]]
    else:
        p[0] = None
def p_dcl_pp(p):
    ''' dcl_pp : COMMA ID LPAREN param_types RPAREN dcl_pp
               |'''
    if(p != None and len(p) > 1):
        if(p[6] != None):
            p[0] = [(p[2], p[4]), *p[6]]
        else:
            p[0] = [(p[2], p[4])]
    else:
        p[0] = None

# var_decl : id [ '[' intcon ']' ]
def p_var_decl(p):
    '''var_decl : ID
       var_decl : ID LSQUARE INTCON RSQUARE'''
    p[0] = VarDecl('var_decl', None, (p[1], p[3] if len(p) > 2 else None),
            p.lexer.lineno)

# parm_types : void
#            | type id [ '[' ']' ] { ',' type id [ '[' ']' ] }
def p_param_types(p):
    '''param_types : VOID
                   | CHAR ID param_types_array param_types_more
                   | INT ID param_types_array param_types_more
                   | FLOAT ID param_types_array param_types_more
                   | CHAR TIMES ID param_types_array param_types_more
                   | INT TIMES ID param_types_array param_types_more
                   | FLOAT TIMES ID param_types_array param_types_more'''
    if(len(p) > 5):
        if(p[5] != None):
            p[0] = ParamTypes('param-types', [(p[2], p[1], p[3], True), *p[4]],
                    None, p.lexer.lineno)
        else:
            p[0] = ParamTypes('param-types', [(p[2], p[1], p[3], True)], None,
                    p.lexer.lineno)
    elif(len(p) > 2):
        if(p[4] != None):
            p[0] = ParamTypes('param-types', [(p[2], p[1], p[3], False),
                *p[4]], None, p.lexer.lineno)
        else:
            p[0] = ParamTypes('param-types', [(p[2], p[1], p[3], False)],
                    None, p.lexer.lineno)
    else:
        p[0] = ParamTypes('param-types-void', None, [p[1]], p.lexer.lineno)
def p_param_types_array(p):
    '''param_types_array : LPAREN RPAREN
                         |'''
    if(len(p) > 2):
        p[0] = "array"
    else:
        p[0] = None
def p_param_types_more(p):
    '''param_types_more : COMMA CHAR ID param_types_array param_types_more
                        | COMMA INT ID param_types_array param_types_more
                        | COMMA FLOAT ID param_types_array param_types_more
                        | COMMA CHAR TIMES ID param_types_array param_types_more
                        | COMMA INT TIMES ID param_types_array param_types_more
                        | COMMA FLOAT TIMES ID param_types_array param_types_more
                        |'''
    if(p != None and len(p) > 6):
        if(p[6] != None):
            p[0] = [(p[4], p[2], p[4], True), *p[5]]
        else:
            p[0] = [(p[4], p[2], p[4], True)]
    elif(p != None and len(p) > 5):
        if(p[5] != None):
            p[0] = [(p[3], p[2], p[4], False), *p[5]]
        else:
            p[0] = [(p[3], p[2], p[4], False)]
    else:
        p[0] = None

# func : type id '(' parm_types ')' '{' { type var_decl { ',' var_decl } ';' } { stmt } '}'
#      | void id '(' parm_types ')' '{' { type var_decl { ',' var_decl } ';' } { stmt } '}'
def p_func(p):
    '''func : CHAR ID LPAREN param_types RPAREN LCURLY func_dcl stmt_repeat RCURLY
            | INT ID LPAREN param_types RPAREN LCURLY func_dcl stmt_repeat RCURLY
            | FLOAT ID LPAREN param_types RPAREN LCURLY func_dcl stmt_repeat RCURLY
            | VOID ID LPAREN param_types RPAREN LCURLY func_dcl stmt_repeat RCURLY'''
    func_vars = p[7] if p[7] != None else None
    func_stmt = p[8] if p[8] != None else None
    p[0] = Func('func', (func_vars, func_stmt), (p[1], p[2], p[4]),
            p.lexer.lineno)
def p_func_dcl(p):
    '''func_dcl : CHAR var_decl func_dcl_p SEMICOLON func_dcl
                | INT var_decl func_dcl_p SEMICOLON func_dcl
                | FLOAT var_decl func_dcl_p SEMICOLON func_dcl
                |'''
    if(p != None and len(p) > 1):
        if(p[3] != None):
            first_var = (p[1], [p[2], *p[3]])
        else:
            first_var = (p[1], [p[2]])
        if(p[5] != None):
            p[0] = [first_var, *p[5]]
        else:
            p[0] = [first_var]
    else:
        p[0] = None
def p_func_dcl_p(p):
    '''func_dcl_p : COMMA var_decl func_dcl_p
                  |'''
    if(p != None and len(p) > 1):
        if(p[3] != None):
            p[0] = [p[2], *p[3]]
        else:
            p[0] = [p[2]]
    else:
        p[0] = None

# stmt : if '(' expr ')' stmt [ else stmt ]
#      | while '(' expr ')' stmt
#      | for '(' [ assg ] ';' [ expr ] ';' [ assg ] ')' stmt
#      | return [ expr ] ';'
#      | assg ';'
#      | id '(' [expr { ',' expr } ] ')' ';'
#      | '{' { stmt } '}'
#      | ';'
def p_stmt_if(p):
    '''stmt : IF LPAREN expr RPAREN stmt stmt_else'''
    if(p[6] != None):
        p[0] = IfStmt('ifstmt-else', [p[5],p[6]], p[3], p.lexer.lineno)
    else:
        p[0] = IfStmt('ifstmt', [p[5]], p[3], p.lexer.lineno)
def p_stmt_else(p):
    '''stmt_else : ELSE stmt
                 |'''
    if(p != None and len(p) > 1):
        p[0] = p[2]
    else:
        p[0] = None
def p_stmt_while(p):
    '''stmt : WHILE LPAREN expr RPAREN stmt'''
    p[0] = WhileStmt('whilestmt', p[5], p[3], p.lexer.lineno)
def p_stmt_for(p):
    '''stmt : FOR LPAREN stmt_opt_assg SEMICOLON stmt_opt_expr SEMICOLON stmt_opt_assg RPAREN stmt'''
    p[0] = ForStmt('forstmt', p[9] ,[p[3],p[5],p[7]], p.lexer.lineno)
def p_stmt_opt_assg(p):
    '''stmt_opt_assg : assg
                     |'''
    if(len(p) > 1):
        p[0] = p[1]
    else:
        p[0]
def p_stmt_opt_expr(p):
    '''stmt_opt_expr : expr
                     |'''
    if(len(p) > 1):
        p[0] = p[1]
    else:
        p[0]
def p_stmt_return(p):
    '''stmt : RETURN stmt_opt_expr SEMICOLON'''
    p[0] = ReturnStmt('returnstmt', None, p[2], p.lexer.lineno)
def p_stmt_assg(p):
    '''stmt : assg SEMICOLON'''
    p[0] = p[1]
def p_stmt_id(p):
    '''stmt : ID LPAREN expr_pp RPAREN SEMICOLON'''
    p[0] = CallStmt('callstmt', p[3], p[1], p.lexer.lineno)
def p_stmt_enclose(p):
    '''stmt : LCURLY stmt_repeat RCURLY'''
    p[0] = StmtEnclose('stmtenclose', p[2], None, p.lexer.lineno)
def p_stmt_repeat(p):
    '''stmt_repeat : stmt stmt_repeat
                   |'''
    if(p != None and len(p) > 1):
        if(p[2] != None):
            p[0] = [p[1], *p[2]]
        else:
            p[0] = [p[1]]
    else:
        p[0] = None
def p_stmt_end(p):
    '''stmt : SEMICOLON'''
    p[0] = None

# assg : id [ '[' expr ']' ] = expr
def p_assg(p):
    '''assg : ID assg_p ASSIGNMENT expr
            | ID PLUS PLUS
            | PLUS PLUS ID
            | ID MINUS MINUS
            | MINUS MINUS ID'''
    if(len(p) > 4):
        p[0] = Assg('Assg', p[4], (p[1], p[2]) , p.lexer.lineno)
    else:
        if(p[3] == "+"):
            p[0] = Assg('Assg-increment', None, (p[1], None), p.lexer.lineno)
        elif(p[3] == "-"):
            p[0] = Assg('Assg-decrement', None, (p[1], None), p.lexer.lineno)
        elif(p[1] == "+"):
            p[0] = Assg('Assg-increment', None, (p[3], None), p.lexer.lineno)
        elif(p[1] == "-"):
            p[0] = Assg('Assg-decrement', None, (p[3], None), p.lexer.lineno)
def p_assg_p(p):
    '''assg_p : LSQUARE expr RSQUARE
            |'''
    if(len(p) > 2):
        p[0] = p[2]
    else:
        p[0] = None

# expr : '–' expr
#      | '!' expr
#      | expr binop expr
#      | expr relop expr
#      | expr logical_op expr
#      | id [ '(' [expr { ',' expr } ] ')' | '[' expr ']' ]
#      | '(' expr ')'
#      | intcon
#      | charcon
#      | stringcon
def p_expr_single(p):
    '''expr : MINUS expr %prec UMINUS
            | NOT expr'''
    p[0] = Expr('expr-not', [p[2]], p[1], p.lexer.lineno)
def p_expr_multi(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr
            | expr EQUAL expr
            | expr NOTEQUAL expr
            | expr LESSEQUAL expr
            | expr LESS expr
            | expr MOREEQUAL expr
            | expr MORE expr
            | expr AND expr
            | expr OR expr'''
    p[0] = Expr('expr', [p[1], p[3]], p[2], p.lexer.lineno)
def p_expr_var_ops(p):
    '''expr : ID PLUS PLUS
            | ID MINUS MINUS
            | PLUS PLUS ID'''
    if(p[2] == "+"):
        if(p[1] == "+"):
            p[0] = Expr('expr-var-pre', None, (p[3], "+"))
        else:
            p[0] = Expr('expr-var-post', None, (p[1], "+"))
    else:
        if(p[1] == "-"):
            p[0] = Expr('expr-var-pre', None, (p[3], "-"))
        else:
            p[0] = Expr('expr-var-post', None, (p[1], "-"))
def p_expr_terminals(p):
    '''expr : INTCON
            | CHARCON
            | STRINGCON
            | FLOATCON'''
    p[0] = Expr('expr-con', None, p[1], p.lexer.lineno)
def p_expr_sub(p):
    '''expr : LPAREN expr RPAREN'''
    p[0] = p[2]
def p_expr_id(p):
    '''expr : ID expr_p'''
    if(p[2] != None and p[2][1] == "("):
        p[0] = Expr('expr-call', [p[2][0]], p[1], p.lexer.lineno)
    elif(p[2] != None):
        p[0] = Expr('expr-arr', p[2][0], p[1], p.lexer.lineno)
    else:
        p[0] = Expr('expr-id', None, p[1], p.lexer.lineno)
def p_expr_p(p):
    '''expr_p : LPAREN expr_pp RPAREN
              | LSQUARE expr RSQUARE
              |'''
    if(p != None and len(p) > 1):
        p[0] = (p[2], p[1])
    else:
        p[0] = None
def p_expr_pp(p):
    '''expr_pp : expr expr_ppp
               |'''
    if(p != None and len(p) > 1):
        if(p[2] != None):
            p[0] = [p[1], *p[2]]
        else:
            p[0] = [p[1]]
    else:
        p[0] = None
def p_expr_ppp(p):
    '''expr_ppp : COMMA expr expr_ppp
                | '''
    if(p != None and len(p) > 1):
        if(p[3] != None):
            p[0] = [p[2], *p[3]]
        else:
            p[0] = [p[2]]
    else:
        p[0] = None

def p_error(p):
    print("Syntax error : line %d" % (p.lineno))
    exit(1)

# Define precedence
precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'EQUAL', 'NOTEQUAL'),
        ('left', 'LESS', 'MORE', 'LESSEQUAL', 'MOREEQUAL'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'UMINUS', 'NOT'),
    )

# Build the parser
parser = yacc.yacc(errorlog=yacc.NullLogger())

result = parser.parse(data, debug=0)
if result == None:
    exit(1)

# Add printf to the function table
class PythonPrint():
    def exe(*args):
        string, *args = args
        string = string[1:-1]
        for i,arg in enumerate(args):
            if type(arg) is list:
                is_str = True
                for c in arg:
                    if type(c) is not str:
                        is_str = False
                        break
                if is_str:
                    str_out = ""
                    for c in arg:
                        str_out = str_out + (c[1:-1] if c != "N/A" else "N/A")
                    args[i] = str_out
                else:
                    args[i] = "MemID: " + str(id(arg))
        print(string % tuple(args))
funcs_global.append(("printf", "void", [], PythonPrint))

for node in result:
    node.prepare()

print_help()
# Start building execution tree
main_function = find_function("main")[3]
main_function.exe([2])

print("End of Program")
while(True):
    execute()

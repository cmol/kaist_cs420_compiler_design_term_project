global funcs_global
global vars_stacks
global vars_global
funcs_global = []
vars_stacks  = []
vars_global  = []

def add_global_vars(var_type, v):
    vars_global.append([var_type,v.ID, v.array])

def add_global_funcs(f):
    funcs_global.append((f.name, f.return_type, f.param_list, f))

def add_vars_stack():
    vars_stacks.append([])

def del_vars_stack():
    vars_stacks.pop()

def push_var(var):
    if var.array:
        vars_stacks[-1].append([var.ID, var.array, []])
    else:
        vars_stacks[-1].append([var.ID, var.array, None])

def find_var(vid):
    for v in vars_stacks[-1]:
        if v[0] == vid:
            return v
    for v in vars_global:
        if v[0] == vid:
            return v
    return None

def assign_var(vid, value, array):
    if array:
        for v in vars_stacks[-1]:
            if v[0] == vid:
                v[2][array] = value
                return
        for v in vars_global:
            if v[0] == vid:
                v[2][array] = value
                return
    else:
        for v in vars_stacks[-1]:
            if v[0] == vid:
                v[2] = value
                return
        for v in vars_global:
            if v[0] == vid:
                v[2] = value
                return

def find_function(fid):
    for f in funcs_global:
        if f[0] == fid:
            return f
    return None

class Node:
    def __init__(self,kind,children=None,leafs=None):
        self.kind = kind
        self.children = children
        self.leafs = leafs

class VarDecl(Node):
    def prepare(self):
        self.ID = self.leafs[0]
        self.array = self.leafs[1]

class Dcl(Node):
    def prepare(self):
        if self.kind == 'dcl-func-extern':
            self.extern = True
            self.type   = self.leafs
            self.funcs  = self.children
            add_functions(self.type, self.funcs, extern=True)
        elif self.kind == 'dcl-func':
            self.extern = False
            self.type   = self.leafs
            self.funcs  = self.children
            add_functions(self.type, self.funcs, extern=False)
        else:
            self.type = self.leafs
            self.vars = self.children
        for var in self.vars:
            if var != None:
                var.prepare()
                add_global_vars(self.type, var)

class ParamTypes(Node):
    params = []
    def prepare(self):
        if self.kind == "param-types-void":
            self.params = [None]
        else:
            self.params = self.children

class Func(Node):
    def prepare(self):
        self.return_type = self.leafs[0]
        self.name        = self.leafs[1]
        self.parameters  = self.leafs[2]
        self.func_vars   = self.children[0]
        self.func_stmts  = self.children[1]

        # Add stack for keeping vars
        add_vars_stack()

        # Parameters
        self.param_list = []
        self.parameters.prepare()
        for param in self.parameters.params:
            if param != None:
                self.param_list.append(param)

        # Internal variables for the function
        for var in self.func_vars:
            for v in var[1]:
                v.prepare()
                push_var(v)

        # Statements for the function
        for stmt in self.func_stmts:
            if stmt != None:
                stmt.prepare()
            else:
                self.func_stmts.remove(stmt)

        # Add function to table
        add_global_funcs(self)

        # Delete variable stack
        del_vars_stack()

class IfStmt(Node):
    def prepare(self):
        self.expr    = self.leafs
        self.stmt_if = self.children[0]
        if self.expr != None:
            self.expr.prepare()
        if self.stmt_if != None:
            self.stmt_if.prepare()
        if self.kind == 'ifstmt-else':
            self.stmt_else = self.children[1]
            if self.stmt_else != None:
                self.stmt_else.prepare()

class WhileStmt(Node):
    def prepare(self):
        self.expr = self.children
        self.stmt = self.leafs
        self.expr.prepare()
        self.stmt.prepare()

class ForStmt(Node):
    def prepare(self):
        self.assignment = self.leafs[0]
        self.expression = self.leafs[1]
        self.operation  = self.leafs[2]
        self.stmt       = self.children
        self.stmt.prepare()

class ReturnStmt(Node):
    def prepare(self):
        self.stmt = self.leafs
        if self.stmt != None:
            self.stmt.prepare()

class Assg(Node):
    def prepare(self):
        self.ID     = self.leafs[0]
        self.array  = self.leafs[1]
        self.assign = self.children
        self.increment = True if self.kind == "Assg-increment" else False

        if not self.increment:
            for assg in self.assign:
                assg.prepare()

        # Type checking
        v = find_var(self.ID)
        if not v or (bool(v[1]) ^ bool(self.array)):
            print("Type error! Cannot find " + str(self.ID))
            print(self.array)
            print("Current var stack: ")
            print(vars_stacks[-1])
            exit(1)


class CallStmt(Node):
    def prepare(self):
        self.function = self.leafs
        self.expr     = self.children
        if self.expr != None:
            if type(self.expr) is list:
                for exp in self.expr:
                    exp.prepare()
            else:
                self.expr.prepare()

        # Type checking
        f = find_function(self.function)
        # Check existence of name
        if not f:
            print("Function " + str(self.function) + " not found")
            exit(1)
        # Check number of arguments
        if (len(f[2]) != len(self.children)
                and f[0] != "printf" and len(self.children) > 1):
            print("Function %s takes %d arguments but %d was given" %
                    (f[0], len(f[2]),len(self.children)))
            exit(1)


class StmtEnclose(Node):
    def prepare(self):
        self.stmts = self.children
        for stmt in self.stmts:
            if stmt != None:
                stmt.prepare()
            else:
                self.stmts.remove(stmt)

class Expr(Node):
    def prepare(self):
        self.exprs = self.children
        self.qualifier = self.leafs
        if self.exprs != None:
            for expr in self.exprs:
                if expr != None:
                    if type(expr) is list:
                        for exp in expr:
                            exp.prepare()
                    else:
                        expr.prepare()

global funcs_global
global vars_stacks
global vars_global
funcs_global = []
vars_stacks  = []
vars_global  = []
default = {
        "int" : 0,
        "float" : 0.0,
        "char" : ''
        }

def add_global_vars(var_type, v):
    """Add variable to global scope"""
    vars_global.append([var_type,v.ID, v.array])

def add_global_funcs(f):
    """Add function to global scope"""
    funcs_global.append((f.name, f.return_type, f.param_list, f))

def add_function_stack():
    """Add overall variable stack for within the function"""
    vars_stacks.append([])

def del_function_stack():
    """Delete the overall variable stack for within the function"""
    vars_stacks.pop()

def add_vars_stack():
    """Add a (perhaps first) sub stack to the function stack"""
    vars_stacks[-1].append([])

def del_vars_stack():
    """Delete the last substack from the function stack"""
    vars_stacks[-1].pop()

def push_var(typ, var):
    """Add a variable to the last stack"""
    if var.array:
        vars_stacks[-1][-1].append([var.ID, typ ,var.array, ["N/A"] * var.array])
    else:
        vars_stacks[-1][-1].append([var.ID, typ ,var.array, "N/A"])

def find_var(vid):
    """Find a variable in the reverse function stacks or in the global stack"""
    for stacks in reversed(vars_stacks[-1]):
        for v in stacks:
            if v[0] == vid:
                return v
    for v in vars_global:
        if v[0] == vid:
            return v
    return None

def assign_var(vid, value, array, index=None):
    """Set variable in the reverse function stack or on the global stack"""
    if array:
        for stacks in reversed(vars_stacks[-1]):
            for v in stacks:
                if v[0] == vid:
                    v[3][index] = value
                    return
        for v in vars_global:
            if v[0] == vid:
                v[3][index] = value
                return
    else:
        for stacks in reversed(vars_stacks[-1]):
            for v in stacks:
                if v[0] == vid:
                    v[3] = value
                    return
        for v in vars_global:
            if v[0] == vid:
                v[3] = value
                return

def find_function(fid):
    """Find function in the function table"""
    for f in funcs_global:
        if f[0] == fid:
            return f
    return None

# Define class for function return
class FunctionReturn(Exception):
    pass

# The node defines a general node structure that all later nodes inharits from.
class Node:
    def __init__(self,kind,children=None,leafs=None,lineno=0):
        self.kind     = kind
        self.children = children
        self.leafs    = leafs
        self.lineno   = lineno

    def __str__(self):
        return self.kind

    def build(self):
        return self

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
        add_function_stack()
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
                push_var(var[0],v)

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
        del_function_stack()

        # Prepare self for execution
        self.build()

    def build(self):
        self.tree = []
        for stmt in self.func_stmts:
            self.tree.append(stmt.build())
        return self

    def exe(self, args=False):
        # Prepare args
        if args:
            args.reverse()

        # Add stack for variables
        add_function_stack()
        add_vars_stack()

        # Find parameters and define them
        for var in self.param_list:
            v = VarDecl("", None, (var[0],var[3]))
            v.prepare()
            push_var(var[1], v)
            assign_var(v.ID, args.pop(), False)

        # Internal variables for the function
        for var in self.func_vars:
            for v in var[1]:
                v.prepare()
                push_var(var[0],v)
        ret = None
        try:
            for node in self.tree:
                print("Exec: " + str(node))
                ret = node.exe()
        except FunctionReturn as ret_val:
            ret = ret_val.args[0]

        del_vars_stack()
        del_function_stack()
        return ret

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

    def exe(self):
        if(self.expr.exe()):
            if(self.stmt_if != None):
                self.stmt_if.exe()
        elif(self.kind == "ifstmt-else" and self.stmt_else != None):
            self.stmt_else.exe()

class WhileStmt(Node):
    def prepare(self):
        self.expr = self.leafs
        self.stmt = self.children
        self.expr.prepare()
        self.stmt.prepare()

    def exe(self):
        res = self.expr.exe()
        while res:
            self.stmt.exe()
            res = self.expr.exe()

class ForStmt(Node):
    def prepare(self):
        self.assignment = self.leafs[0]
        self.expression = self.leafs[1]
        self.operation  = self.leafs[2]
        self.stmt       = self.children
        self.assignment.prepare()
        self.expression.prepare()
        self.operation.prepare()
        self.stmt.prepare()

    def exe(self):
        self.assignment.exe()
        res = self.expression.exe()
        while res:
            self.stmt.exe()
            self.operation.exe()
            res = self.expression.exe()

class ReturnStmt(Node):
    def prepare(self):
        self.stmt = self.leafs
        if self.stmt != None:
            self.stmt.prepare()

    def exe(self):
        if self.stmt != None:
            raise FunctionReturn(self.stmt.exe())
        else:
            raise FunctionReturn(None)

class Assg(Node):
    def prepare(self):
        self.ID     = self.leafs[0]
        self.array  = self.leafs[1]
        self.assign = self.children
        self.increment = True if self.kind == "Assg-increment" else False

        if not self.increment:
            #for assg in self.assign:
            self.assign.prepare()
        if self.array != None:
            self.array.prepare()

        # Type checking
        v = find_var(self.ID)
        if not v or (bool(v[2]) ^ bool(self.array)):
            print("Type error! Cannot find " + str(self.ID))
            print(self.array)
            print("Current var stack: ")
            print(vars_stacks[-1])
            exit(1)

    def exe(self):
        v = find_var(self.ID)
        if self.increment:
            assign_var(self.ID, v[3] + 1, False)
        else:
            if self.array != None:
                assign_var(self.ID, self.assign.exe(), True, self.array.exe())
            else:
                assign_var(self.ID, self.assign.exe(), False)

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

    def exe(self, *args):
        args = []
        for exp in self.expr:
            args.append(exp.exe())
        f = find_function(self.function)
        f[3].exe(*args)

class StmtEnclose(Node):
    def prepare(self):
        self.stmts = self.children
        for stmt in self.stmts:
            if stmt != None:
                stmt.prepare()
            else:
                self.stmts.remove(stmt)

    def exe(self):
        add_vars_stack()
        print("All in enclose: " + str(self.stmts))
        for stmt in self.stmts:
            print("Enclose: " + str(stmt))
            stmt.exe()
        del_vars_stack()

class Expr(Node):
    def prepare(self):
        self.exprs = self.children
        self.qualifier = self.leafs
        if self.exprs != None:
            if type(self.exprs) is not list:
                self.exprs = [self.exprs]
            for expr in self.exprs:
                if expr != None:
                    if type(expr) is list:
                        for exp in expr:
                            exp.prepare()
                    else:
                        expr.prepare()

    def exe(self):
        if self.kind == "expr-con":
            return self.qualifier
        elif self.kind == "expr-id":
            var = find_var(self.qualifier)
            return var[3] if var[3] != "N/A" else default[var[1]]
        elif self.kind == "expr-call":
            args = []
            for exp in self.exprs[0]:
                args.append(exp.exe())
            f = find_function(self.qualifier)
            return f[3].exe(args)
        elif self.kind == "expr-arr":
            var = find_var(self.qualifier)
            index = self.exprs[0].exe()
            if var[3][index] != "N/A":
                return var[3][index]
            else:
                return default[var[1]]
        elif self.kind == "expr-not":
            if self.qualifier == "-":
                return expr.exe() * -1
            else:
                return not expr.exe()
        elif self.qualifier == "+":
            return self.exprs[0].exe() + self.exprs[1].exe()
        elif self.qualifier == "-":
            return self.exprs[0].exe() - self.exprs[1].exe()
        elif self.qualifier == "*":
            return self.exprs[0].exe() * self.exprs[1].exe()
        elif self.qualifier == "/":
            return self.exprs[0].exe() / self.exprs[1].exe()
        elif self.qualifier == "==":
            return self.exprs[0].exe() == self.exprs[1].exe()
        elif self.qualifier == "!=":
            return self.exprs[0].exe() != self.exprs[1].exe()
        elif self.qualifier == "<=":
            return self.exprs[0].exe() <= self.exprs[1].exe()
        elif self.qualifier == "<":
            return self.exprs[0].exe() < self.exprs[1].exe()
        elif self.qualifier == ">=":
            return self.exprs[0].exe() >= self.exprs[1].exe()
        elif self.qualifier == ">":
            return self.exprs[0].exe() > self.exprs[1].exe()
        elif self.qualifier == "&&":
            return self.exprs[0].exe() and self.exprs[1].exe()
        elif self.qualifier == "||":
            return self.exprs[0].exe() or self.exprs[1].exe()


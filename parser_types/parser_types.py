def add_global_vars(var_type, var):
    pass
def add_global_funcs(**args):
    pass
def add_vars_stacks(**args):
    pass


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
#    def __init__(self,*args):
#        super().__init__(**locals())
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
            add_global_vars(self.type, self.vars)
        for child in self.children:
            if child != None:
                child.prepare()

class ParamTypes(Node):
    pass
#    def __init__(self,*args):
#        super().__init__(**locals())

class Func(Node):
    def prepare(self):
        self.return_type = self.leafs[0]
        self.name        = self.leafs[1]
        self.parameters  = self.leafs[2]
        self.func_vars   = self.children[0]
        self.func_stmts  = self.children[1]

        for var in self.func_vars:
            for v in var[1]:
                v.prepare()
        for stmt in self.func_stmts:
            if stmt != None:
                stmt.prepare()
            else:
                self.func_stmts.remove(stmt)

class IfStmt(Node):
    def prepare(self):
        self.expr    = self.leafs
        self.stmt_if = self.children[0]
        self.stmt_if.prepare()
        if self.kind == 'ifstmt-else':
            self.stmt_else = self.children[1]
            self.stmt_else.prepare()

class WhileStmt(Node):
    pass
#    def __init__(self,*args):
#        super().__init__(**locals())

class ForStmt(Node):
    def prepare(self):
        self.assignment = self.leafs[0]
        self.expression = self.leafs[1]
        self.operation  = self.leafs[2]
        self.stmt       = self.children
        self.stmt.prepare()

class ReturnStmt(Node):
    pass
#    def __init__(self,*args):
#        super().__init__(**locals())

class Assg(Node):
    def prepare(self):
        print(self.leafs)
        self.ID     = self.leafs[0]
        self.array  = self.leafs[1]
        self.assign = self.children
        for assg in self.assign:
            assg.prepare()

class CallStmt(Node):
    pass
#    def __init__(self,*args):
#        super().__init__(**locals())

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
            for expr in exprs:
                expr.prepare()

class Node:
    def __init__(self,kind,children=None,leaf=None):
        self.kind = kind
        self.children = children
        self.leaf = leaf

class BinOP(Node):
    pass
#    def __init__(self,*args):
#        super().__init__(**locals())

class Prog(Node):
    pass
#    def __init__(self,*args):
#        super().__init__(**locals())

class Type(Node):
    pass
#    def __init__(self,*args):
#        super().__init__(**locals())

class VarDecl(Node):
    pass
#    def __init__(self,*args):
#        super().__init__(**locals())

class Dcl(Node):
    pass
#    def __init__(self,*args):
#        super().__init__(**locals())

class ParamTypes(Node):
    pass
#    def __init__(self,*args):
#        super().__init__(**locals())

class Func(Node):
    pass
#    def __init__(self,*args):
#        super().__init__(**locals())

class IfStmt(Node):
    pass
#    def __init__(self,*args):
#        super().__init__(**locals())

class WhileStmt(Node):
    pass
#    def __init__(self,*args):
#        super().__init__(**locals())

class ForStmt(Node):
    pass
#    def __init__(self,*args):
#        super().__init__(**locals())

class ReturnStmt(Node):
    pass
#    def __init__(self,*args):
#        super().__init__(**locals())

class Assg(Node):
    pass
#    def __init__(self,*args):
#        super().__init__(**locals())

class CallStmt(Node):
    pass
#    def __init__(self,*args):
#        super().__init__(**locals())

class StmtEnclose(Node):
    pass
#    def __init__(self,*args):
#        super().__init__(**locals())

class Expr(Node):
    pass
#    def __init__(self,*args):
#        super().__init__(**locals())

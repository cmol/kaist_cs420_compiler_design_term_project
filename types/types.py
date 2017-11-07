class Node:
    def __init__(self,kind,children=None,leaf=None):
        self.kind = kind
        self.children = children
        self.leaf = leaf

class BinOP(Node):
    def __init__(self,*args):
        super().__init__(**locals())

class Prog(Node):
    def __init__(self,*args):
        super().__init__(**locals())


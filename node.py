class Node:
    i = 0

    def newId():
        Node.i += 1
        return Node.i
    
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, SymbolTable):
        pass
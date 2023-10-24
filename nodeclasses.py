from node import Node

class BinOp(Node):
    def Evaluate(self, SymbolTable):
        child_0 = self.children[0].Evaluate(SymbolTable)
        child_1 = self.children[1].Evaluate(SymbolTable)
        if child_0[1] == child_1[1]:
            if self.value == "PLUS": 
                subchild = child_0[0] + child_1[0]
                return (subchild, "int")
            if self.value == "MINUS":   
                subchild = child_0[0] - child_1[0]
                return (subchild, "int")
            if self.value == "MULT":   
                subchild = child_0[0] * child_1[0]
                return (subchild, "int")
            if self.value == "DIV":   
                subchild = child_0[0] // child_1[0]
                return (subchild, "int")
            if self.value == "AND":
                subchild = child_0[0] and child_1[0] 
                if (subchild == True):
                    return (1, "int")
                elif (subchild == False):
                    return (0, "int")
                else:
                    raise Exception("Tipos incompativeis")
            if self.value == "OR":   
                subchild = child_0[0] or child_1[0] 
                if (subchild == True):
                    return (1, "int")
                elif (subchild == False):
                    return (0, "int")
                else:
                    raise Exception("Tipos incompativeis")
            if self.value == "EQUALTO": 
                subchild = child_0[0] == child_1[0]
                if (subchild == True):
                    return (1, "int")
                elif (subchild == False):
                    return (0, "int")
                else:
                    raise Exception("Tipos incompativeis")
            if self.value == "GREATERTHAN":   
                subchild = child_0[0] > child_1[0] 
                if (subchild == True):
                    return (1, "int")
                elif (subchild == False):
                    return (0, "int")
                else:
                    raise Exception("Tipos incompativeis")
            if self.value == "LOWERTHAN": 
                subchild = child_0[0] < child_1[0] 
                if (subchild == True):
                    return (1, "int")
                elif (subchild == False):
                    return (0, "int")
                else:
                    raise Exception("Tipos incompativeis")
            if self.value == "DOT":
                subchild = str(child_0[0]) + str(child_1[0])
                return (subchild, "string")
        elif self.value == "DOT":
            subchild = str(child_0[0]) + str(child_1[0])
            return (subchild, "string")
        else:
            raise Exception("Operacao invalida")

class UnOp(Node):
    def Evaluate(self, SymbolTable):
        if self.value == "PLUS":   
            return (self.children[0].Evaluate(SymbolTable)[0], "int")
        elif self.value == "MINUS": 
            negative = -self.children[0].Evaluate(SymbolTable)[0] 
            return (negative, "int")
        elif self.value == "NOT":
            bol = not self.children[0].Evaluate(SymbolTable)[0]
            if (bol == True):
                return (1, "int")
            elif (bol == False):
                return (0, "int")
            else:
                raise Exception("Not nao se aplica")
            

class IntVal(Node):
    def Evaluate(self, SymbolTable):
        return (self.value, "int")
    
class StrVal(Node):
    def Evaluate(self, SymbolTable):
        return (self.value, "string")
    
class VarDec(Node):
    def Evaluate(self, SymbolTable):
        if self.children[2] != None:
            SymbolTable.create_ST(self.children[0], self.children[1], self.children[2].Evaluate(SymbolTable)[0])
        else:
            SymbolTable.create_ST(self.children[0], self.children[1], None)

class NoOp(Node):
    def Evaluate(self, SymbolTable):
        pass

class Identifier(Node):
    def Evaluate(self, SymbolTable):
        return SymbolTable.get_ST(self.value)

class Assignment(Node):
    def Evaluate(self, SymbolTable):
        SymbolTable.set_ST(self.children[0].value, self.children[1].Evaluate(SymbolTable))


class Block(Node):
    def Evaluate(self, SymbolTable):
        for child in self.children:
            child.Evaluate(SymbolTable)
        
class Println(Node):
    def Evaluate(self, SymbolTable):
        print(self.children[0].Evaluate(SymbolTable)[0]) 

class If(Node):
    def Evaluate(self, SymbolTable):
        if self.children[0].Evaluate(SymbolTable):
            return self.children[1].Evaluate(SymbolTable)
        else:
            if len(self.children) > 2:
                return self.children[2].Evaluate(SymbolTable)

class For(Node):
    def Evaluate(self, SymbolTable):
        self.children[0].Evaluate(SymbolTable)
        while (self.children[1].Evaluate(SymbolTable)[0] == 1):
            self.children[3].Evaluate(SymbolTable)
            self.children[2].Evaluate(SymbolTable)
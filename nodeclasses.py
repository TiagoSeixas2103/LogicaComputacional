from node import Node
from symboltable import SymbolTable

class BinOp(Node):
    def Evaluate(self, SymbolTable, FuncTable):
        child_0 = self.children[0].Evaluate(SymbolTable, FuncTable)
        child_1 = self.children[1].Evaluate(SymbolTable, FuncTable)
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
    def Evaluate(self, SymbolTable, FuncTable):
        if self.value == "PLUS":   
            return (self.children[0].Evaluate(SymbolTable, FuncTable)[0], "int")
        elif self.value == "MINUS": 
            negative = -self.children[0].Evaluate(SymbolTable, FuncTable)[0] 
            return (negative, "int")
        elif self.value == "NOT":
            bol = not self.children[0].Evaluate(SymbolTable, FuncTable)[0]
            if (bol == True):
                return (1, "int")
            elif (bol == False):
                return (0, "int")
            else:
                raise Exception("Not nao se aplica")


class IntVal(Node):
    def Evaluate(self, SymbolTable, FuncTable):
        return (self.value, "int")

class StrVal(Node):
    def Evaluate(self, SymbolTable, FuncTable):
        return (self.value, "string")

class VarDec(Node):
    def Evaluate(self, SymbolTable, FuncTable):
        if self.value == "FUNCTION_VARIABLE":
            FuncTable.create_ST(self.children[0], self.children[1], None)
            return self.children[0]
        else:
            if self.children[2] != None:
                SymbolTable.create_ST(self.children[0], self.children[1], self.children[2].Evaluate(SymbolTable, FuncTable)[0])
                return self.children[0]
            else:
                SymbolTable.create_ST(self.children[0], self.children[1], None)
                return self.children[0]

class NoOp(Node):
    def Evaluate(self, SymbolTable, FuncTable):
        pass

class Identifier(Node):
    def Evaluate(self, SymbolTable, FuncTable):
        return SymbolTable.get_ST(self.value)

class Assignment(Node):
    def Evaluate(self, SymbolTable, FuncTable):
        SymbolTable.set_ST(self.children[0].value, self.children[1].Evaluate(SymbolTable, FuncTable))


class Block(Node):
    def Evaluate(self, SymbolTable, FuncTable):
        for child in self.children:
            child.Evaluate(SymbolTable, FuncTable)

class Println(Node):
    def Evaluate(self, SymbolTable, FuncTable):
        print(self.children[0].Evaluate(SymbolTable, FuncTable)[0]) 

class If(Node):
    def Evaluate(self, SymbolTable, FuncTable):
        if self.children[0].Evaluate(SymbolTable, FuncTable):
            return self.children[1].Evaluate(SymbolTable, FuncTable)
        else:
            if len(self.children) > 2:
                return self.children[2].Evaluate(SymbolTable, FuncTable)

class For(Node):
    def Evaluate(self, SymbolTable, FuncTable):
        self.children[0].Evaluate(SymbolTable, FuncTable)
        while (self.children[1].Evaluate(SymbolTable, FuncTable)[0] == 1):
            self.children[3].Evaluate(SymbolTable, FuncTable)
            self.children[2].Evaluate(SymbolTable, FuncTable)

class FuncDec(Node):
    def Evaluate(self, SymbolTable, FuncTable):
        child_0 = self.children[0].Evaluate(SymbolTable, FuncTable)
        FuncTable.set_ST(child_0, self)

class FuncCall(Node):
    def Evaluate(self, ST, FuncTable):
        node, type = FuncTable.get_ST(self.value)
        funcSymbolTable = SymbolTable()
        if len(node.children) > 2:
            for i in range(len(node.children) - 2):
                vardec = node.children[i+1].Evaluate(funcSymbolTable, FuncTable)
                child_i = self.children[i].Evaluate(ST, FuncTable)
                funcSymbolTable.set_ST(vardec, child_i)
        
        node.children[-1].Evaluate(funcSymbolTable, FuncTable)
        return_value = funcSymbolTable.get_ST("RETURN")
        return return_value

class FuncReturn(Node):
    def Evaluate(self, SymbolTable, FuncTable):
        child_0 = self.children[0].Evaluate(SymbolTable, FuncTable)
        SymbolTable.create_ST(self.value, child_0[1], child_0[0]) 
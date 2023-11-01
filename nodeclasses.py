from node import Node
from write import WriteASM

class BinOp(Node):
    def Evaluate(self, SymbolTable):
        child_1 = self.children[1].Evaluate(SymbolTable)
        string = "PUSH EAX ; BinOp guarda o resultado na pilha\n\n"
        WriteASM.write(string)
        child_0 = self.children[0].Evaluate(SymbolTable)
        string = "POP EBX ; BinOp recupera o valor da pilha\n"
        WriteASM.write(string)
        if child_0[1] == child_1[1]:
            if self.value == "PLUS": 
                string = "ADD EAX, EBX ; O BinOp soma EAX e EBX, e guarda em EAX\n"
                WriteASM.write(string)
                subchild = child_0[0] + child_1[0]
                return (subchild, "int")
            if self.value == "MINUS": 
                string = "SUB EAX, EBX ; O BinOp subtrai EAX e EBX, e guarda em EAX\n"
                WriteASM.write(string)  
                subchild = child_0[0] - child_1[0]
                return (subchild, "int")
            if self.value == "MULT":   
                string = "IMUL EBX ; O BinOp multiplica EAX por EBX, e guarda em EAX\n"
                WriteASM.write(string)
                subchild = child_0[0] * child_1[0]
                return (subchild, "int")
            if self.value == "DIV":   
                string = "IDIV EBX ; O BinOp divide EAX por EBX, e guarda em EAX\n"
                WriteASM.write(string)
                subchild = child_0[0] // child_1[0]
                return (subchild, "int")
            if self.value == "AND":
                string = "AND EAX, EBX ; O BinOp relaciona EAX e EBX, e guarda em EAX\n"
                WriteASM.write(string)
                subchild = child_0[0] and child_1[0] 
                if (subchild == True):
                    return (1, "int")
                elif (subchild == False):
                    return (0, "int")
                else:
                    raise Exception("Tipos incompativeis")
            if self.value == "OR":   
                string = "OR EAX, EBX ; O BinOp relaciona EAX e EBX, e guarda em EAX\n"
                WriteASM.write(string)
                subchild = child_0[0] or child_1[0] 
                if (subchild == True):
                    return (1, "int")
                elif (subchild == False):
                    return (0, "int")
                else:
                    raise Exception("Tipos incompativeis")
            if self.value == "EQUALTO": 
                string = "CMP EAX, EBX ;\n"
                WriteASM.write(string) 
                string = "CALL binop_je ;\n\n"
                WriteASM.write(string) 
                subchild = child_0[0] == child_1[0]
                if (subchild == True):
                    return (1, "int")
                elif (subchild == False):
                    return (0, "int")
                else:
                    raise Exception("Tipos incompativeis")
            if self.value == "GREATERTHAN":  
                string = "CMP EAX, EBX ;\n"
                WriteASM.write(string) 
                string = "CALL binop_jg ;\n\n"
                WriteASM.write(string) 
                subchild = child_0[0] > child_1[0] 
                if (subchild == True):
                    return (1, "int")
                elif (subchild == False):
                    return (0, "int")
                else:
                    raise Exception("Tipos incompativeis")
            if self.value == "LOWERTHAN":
                string = "CMP EAX, EBX ;\n"
                WriteASM.write(string) 
                string = "CALL binop_jl ;\n\n"
                WriteASM.write(string)  
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
        if self.children != None and self.children[0] == "scan":
            string = "\nPUSH scanint ; endereco de memoria de suporte\n"
            WriteASM.write(string)
            string = "PUSH formatin ; formato de entrada (int)\n"
            WriteASM.write(string)
            string = "call scanf\n"
            WriteASM.write(string)
            string = "ADD ESP, 8 ; Remove os argumentos da pilha\n\n"
            WriteASM.write(string)
            string = "MOV EAX, DWORD [scanint] ; retorna o valor lido em EAX\n\n"
            WriteASM.write(string)
        else:
            string = "MOV EAX, " + str(self.value) + " ; Evaluate do IntVal\n"
            WriteASM.write(string)
        return (self.value, "int")
    
class StrVal(Node):
    def Evaluate(self, SymbolTable):
        return (self.value, "string")
    
class VarDec(Node):
    def Evaluate(self, SymbolTable):
        string = "PUSH DWORD 0 ; Aloca Espaço\n"
        WriteASM.write(string)
        if self.children[2] != None:
            child2 = self.children[2].Evaluate(SymbolTable)
            SymbolTable.create_ST(self.children[0], self.children[1], child2[0])
            valor = SymbolTable.get_ST(self.children[0])
            string = "MOV [EBP-" + str(valor[2]) + "], EAX ; resultado da atribuição\n\n"
            WriteASM.write(string)
        else:
            SymbolTable.create_ST(self.children[0], self.children[1], None)

class NoOp(Node):
    def Evaluate(self, SymbolTable):
        pass

class Identifier(Node):
    def Evaluate(self, SymbolTable):
        valor = SymbolTable.get_ST(self.value)
        string = "MOV EAX, [EBP-" + str(valor[2]) + "] ; Evaluate do Identifier\n\n"
        WriteASM.write(string)
        return valor

class Assignment(Node):
    def Evaluate(self, SymbolTable):
        SymbolTable.set_ST(self.children[0].value, self.children[1].Evaluate(SymbolTable))
        valor = SymbolTable.get_ST(self.children[0].value)
        string = "MOV [EBP-" + str(valor[2]) + "], EAX ; resultado da atribuição\n\n"
        WriteASM.write(string)


class Block(Node):
    def Evaluate(self, SymbolTable):
        for child in self.children:
            child.Evaluate(SymbolTable)
        
class Println(Node):
    def Evaluate(self, SymbolTable):
        string = "\n"
        WriteASM.write(string)
        #print(self.children[0].Evaluate(SymbolTable)[0]) 
        self.children[0].Evaluate(SymbolTable)
        string = "PUSH EAX ; Empilha os argumentos para chamar a funcao\n"
        WriteASM.write(string)
        string = "PUSH formatout ; Dizendo para o printf que é um inteiro\n"
        WriteASM.write(string)
        string = "CALL printf ; Chamada da funcao\n"
        WriteASM.write(string)
        string = "ADD ESP, 8 ; Remove os argumentos da pilha\n\n"
        WriteASM.write(string)

class If(Node):
    def Evaluate(self, SymbolTable):
        #if self.children[0].Evaluate(SymbolTable):
        #    return self.children[1].Evaluate(SymbolTable)
        #else:
        #    if len(self.children) > 2:
        #        return self.children[2].Evaluate(SymbolTable)
        self.children[0].Evaluate(SymbolTable)
        string = "CMP EAX, True ; \n"
        WriteASM.write(string)
        id = Node.newId()
        string = "JNE LABEL_ELSE_" + str(id) +"\n"
        WriteASM.write(string)
        self.children[1].Evaluate(SymbolTable)
        string = "JMP EXIT ; \n"
        WriteASM.write(string)
        string = "LABEL_ELSE_" + str(id) +":\n"
        WriteASM.write(string)
        if len(self.children) > 2:
            childELSE = self.children[2].Evaluate(SymbolTable)
            print(childELSE)
        string = "EXIT:\n\n"
        WriteASM.write(string)


class For(Node):
    def Evaluate(self, SymbolTable):
        self.children[0].Evaluate(SymbolTable)
        id = Node.newId()
        string = "LOOP_" + str(id) +":\n\n"
        WriteASM.write(string)
        #while (self.children[1].Evaluate(SymbolTable)[0] == 1):
        #    self.children[3].Evaluate(SymbolTable)
        #    self.children[2].Evaluate(SymbolTable)
        self.children[1].Evaluate(SymbolTable)
        string = "CMP EAX, False ; \n"
        WriteASM.write(string)
        string = "JE EXIT_" + str(id) +" ; \n\n"
        WriteASM.write(string)
        self.children[3].Evaluate(SymbolTable)
        self.children[2].Evaluate(SymbolTable)
        string = "JMP LOOP_" + str(id) +" ; \n"
        WriteASM.write(string)
        string = "EXIT_" + str(id) +":\n"
        WriteASM.write(string)
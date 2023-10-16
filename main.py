import sys

class Token:
    def __init__(self, type, value):
        self.type = str (type)
        self.value = None

class PrePro:
    def __init__(self, source, position):
        self.source = source
        self.position = int (position)

    def filter(self):
        file = open(self.source, "r")
        linhas = file.readlines()
        novas_linhas = []
        for linha in linhas:
            if "//" in linha:
                novas_linhas.append(linha.split('//')[0] + "\n")
            else:
                novas_linhas.append(linha)
        texto = "".join(novas_linhas)
        return texto

class Tokenizer:
    def __init__(self, source, position, next):
        self.source = str (source)
        self.position = int (position)
        self.next = Token("", None)
        self.palavras_reservadas = {
            "Println" : "PRINT",
            "Scanln" : "SCAN",
            "if" : "IF",
            "for" : "FOR",
            "else" : "ELSE",
            "var" : "VARIABLE",
            "int" : "INTTYPE",
            "string" : "STRINGTYPE",
        }
        self.tipos = {
            "+" : "PLUS",
            "-" : "MINUS",
            "*" : "MULT",
            "/" : "DIV",
            "(" : "OPENPAR",
            ")" : "CLOSEPAR",
            "\n" : "ENTER",
            ">" : "GREATERTHAN",
            "<" : "LOWERTHAN",
            "!" : "NOT",
            "{" : "OPENKEY",
            "}" : "CLOSEKEY",
            ";" : "SEMICOLON",
            "." : "DOT",
        }

    def selectNext(self):
        whitespaces = {
            " " : "SPACE",
            "\t" : "TAB",
        }
        while self.position < len(self.source) and self.source[self.position] in whitespaces:
            self.position += 1
            
        if self.position < len(self.source):
            if self.source[self.position].isdigit():
                self.next.type = "INT"
                posicao = self.position+1
                string = self.source[self.position]
                while posicao < len(self.source) and self.source[posicao].isdigit():
                    string += self.source[posicao]
                    posicao +=1
                self.next.value = int(string)
                self.position = posicao - 1
            elif self.source[self.position].islower() or self.source[self.position].isupper():
                posicao = self.position+1
                string = self.source[self.position]
                while posicao < len(self.source) and (self.source[posicao].isdigit() or self.source[posicao].isalpha() or self.source[posicao] == "_"):
                    string += self.source[posicao]
                    posicao +=1
                self.next.value = string
                if string in self.palavras_reservadas:
                    self.next.type = self.palavras_reservadas[string]
                else:
                    self.next.type = "IDENTIFIER"
                self.position = posicao - 1
            elif self.source[self.position] == "=":
                if self.source[self.position + 1] == "=":
                    self.position += 1
                    self.next.type = "EQUALTO"
                    self.next.value = None
                else:
                    self.next.type = "EQUAL"
                    self.next.value = None
            elif self.source[self.position] == "&":
                if self.source[self.position+1] == "&":
                    self.position += 1
                    self.next.type = "AND"
                    self.next.value = None
            elif self.source[self.position] == "|":
                if self.source[self.position+1] == "|":
                    self.position += 1
                    self.next.type = "OR"
                    self.next.value = None
            elif self.source[self.position] in self.tipos.keys():
                self.next.type = self.tipos[self.source[self.position]]
                self.next.value = None
            elif self.source[self.position] == '"':
                self.position += 1
                string = ""
                while self.position < len(self.source) and (self.source[self.position] != '"' and self.source[self.position] != '\n'):
                    string += self.source[self.position]
                    self.position +=1
                if self.source[self.position] == '"':
                    self.next.value = string
                    self.next.type = "STRING"
                else:
                    raise Exception("Nao fechou string")
            else:
                self.next.type = "ERROR"
                self.next.value = None
            self.position += 1
        else:
            self.next.type = "EOF"
            self.next.value = None

class SymbolTable:
    def __init__(self):
        self.dicionario = {}
        self.type = {}

    def get_ST(self, id):
        if id in self.dicionario and id in self.type:
            return (self.dicionario[id], self.type[id])
        else:
            raise Exception("Nao esta na Symbol Table")
    
    def set_ST(self, id, value):
        if id in self.type:
            if self.type[id] == value[1]:
                self.dicionario[id] = value[0]
            else:
                raise Exception("Variavel do tipo errado")
        else:
            raise Exception("Variavel nao declarada")

    def create_ST(self, id, type, value):
        if id not in self.dicionario:
            self.dicionario[id] = value
            self.type[id] = type
        else:
            raise Exception("variavel ja declarada")


class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, SymbolTable):
        pass
    
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
        while (self.children[1].Evaluate(SymbolTable)):
            self.children[3].Evaluate(SymbolTable)
            self.children[2].Evaluate(SymbolTable)

class Parser:
    tokenizer = Tokenizer("", 0, Token("", None))
    def parseFactor():       
        if Parser.tokenizer.next.type == "INT":
            resultado = IntVal(Parser.tokenizer.next.value, None)
            Parser.tokenizer.selectNext()
            return resultado
        if Parser.tokenizer.next.type == "STRING":
            resultado = StrVal(Parser.tokenizer.next.value, None)
            Parser.tokenizer.selectNext()
            return resultado
        elif Parser.tokenizer.next.type == "IDENTIFIER":
            resultado = Identifier(Parser.tokenizer.next.value, None)
            Parser.tokenizer.selectNext()
            return resultado
        elif Parser.tokenizer.next.type == "PLUS":
            Parser.tokenizer.selectNext()
            resultado = UnOp("PLUS", [Parser.parseFactor()])
            return resultado
        elif Parser.tokenizer.next.type == "MINUS":
            Parser.tokenizer.selectNext()
            resultado = UnOp("MINUS", [Parser.parseFactor()])
            return resultado
        elif Parser.tokenizer.next.type == "NOT":
            Parser.tokenizer.selectNext()
            resultado = UnOp("NOT", [Parser.parseFactor()])
            return resultado
        elif Parser.tokenizer.next.type == "OPENPAR":
            Parser.tokenizer.selectNext()
            resultado = Parser.parseBoolExpression()
            if Parser.tokenizer.next.type == "CLOSEPAR":
                Parser.tokenizer.selectNext()
                return resultado
            raise Exception("Nao fechou parenteses")
        elif Parser.tokenizer.next.type == "SCAN":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "OPENPAR":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "CLOSEPAR":
                    Parser.tokenizer.selectNext()
                    resultado = IntVal(int(input()), None)
                    return resultado
                raise Exception("Nao fechou parenteses no scan")
            raise Exception("Nao abriu parenteses no scan")
        else:
           raise Exception("Nao foi factor") 

    def parseTerm():
        resultado = Parser.parseFactor() 
        while Parser.tokenizer.next.type == "MULT" or Parser.tokenizer.next.type == "DIV":
            if Parser.tokenizer.next.type == "MULT":
                Parser.tokenizer.selectNext()
                resultado  = BinOp("MULT",[resultado, Parser.parseFactor()])
            if Parser.tokenizer.next.type == "DIV":
                Parser.tokenizer.selectNext()
                resultado  = BinOp("DIV",[resultado, Parser.parseFactor()])
        return resultado

    def parseExpression():
        resultado = Parser.parseTerm() 
        dict = {
            "PLUS" : "PLUS",
            "MINUS" : "MINUS",
            "DOT" : "DOT",
            }
        while Parser.tokenizer.next.type in dict:
            if Parser.tokenizer.next.type == "PLUS":
                Parser.tokenizer.selectNext()
                resultado = BinOp("PLUS",[resultado, Parser.parseTerm()])
            if Parser.tokenizer.next.type == "MINUS":
                Parser.tokenizer.selectNext()
                resultado = BinOp("MINUS",[resultado, Parser.parseTerm()])
            if Parser.tokenizer.next.type == "DOT":
                Parser.tokenizer.selectNext()
                resultado = BinOp("DOT",[resultado, Parser.parseTerm()])
        return resultado
    
    def parseRelationalExpression():
        resultado = Parser.parseExpression()
        condicao = Parser.tokenizer.next.type 
        while condicao == "EQUALTO" or condicao == "GREATERTHAN" or condicao == "LOWERTHAN":
            if Parser.tokenizer.next.type == "EQUALTO":
                Parser.tokenizer.selectNext()
                resultado = BinOp("EQUALTO",[resultado, Parser.parseExpression()])
            if Parser.tokenizer.next.type == "GREATERTHAN":
                Parser.tokenizer.selectNext()
                resultado = BinOp("GREATERTHAN",[resultado, Parser.parseExpression()])
            if Parser.tokenizer.next.type == "LOWERTHAN":
                Parser.tokenizer.selectNext()
                resultado = BinOp("LOWERTHAN",[resultado, Parser.parseExpression()])
            condicao = Parser.tokenizer.next.type
        return resultado

    def parseBoolTerm():
        resultado = Parser.parseRelationalExpression() 
        while Parser.tokenizer.next.type == "AND":
            Parser.tokenizer.selectNext()
            resultado = BinOp("AND",[resultado, Parser.parseRelationalExpression()])
        return resultado
    
    def parseBoolExpression():
        resultado = Parser.parseBoolTerm() 
        while Parser.tokenizer.next.type == "OR":
            Parser.tokenizer.selectNext()
            resultado = BinOp("OR",[resultado, Parser.parseBoolTerm()])
        return resultado
    
    def parseStatement():
        resultado = NoOp(None, [])
        if Parser.tokenizer.next.type == "ENTER":
            Parser.tokenizer.selectNext()
            return resultado
        
        elif Parser.tokenizer.next.type == "IDENTIFIER":
            valor_ident = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "EQUAL":
                Parser.tokenizer.selectNext()
                resultado = Assignment("EQUAL", [Identifier(valor_ident, None), Parser.parseBoolExpression()])
                if Parser.tokenizer.next.type == "ENTER":
                    Parser.tokenizer.selectNext()
                    return resultado
                raise Exception("Nao deu Enter depois do assignment")
            raise Exception("Nao botou igual ou sinal")
        
        elif Parser.tokenizer.next.type == "PRINT":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "OPENPAR":
                Parser.tokenizer.selectNext()
                resultado = Println("PRINT", [Parser.parseBoolExpression()])
                if Parser.tokenizer.next.type == "CLOSEPAR":
                    Parser.tokenizer.selectNext()
                    #if Parser.tokenizer.next.type == "ENTER":
                    #    Parser.tokenizer.selectNext()
                    return resultado
                    #raise Exception("Nao deu Enter depois do print")
                raise Exception("Nao fechou parenteses")
            raise Exception("Nao abriu parenteses")
        
        elif Parser.tokenizer.next.type == "IF":
            Parser.tokenizer.selectNext()
            condition = Parser.parseBoolExpression()
            block = Parser.parseBlock()
            resultado = If("IF", [condition, block])
            if Parser.tokenizer.next.type == "ELSE":
                Parser.tokenizer.selectNext()
                newBlock = Parser.parseBlock()
                resultado.children.append(newBlock)
            if Parser.tokenizer.next.type == "ENTER":
                Parser.tokenizer.selectNext()
                return resultado
            raise Exception("faltou Enter depois do if")
        
        elif Parser.tokenizer.next.type == "FOR":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "IDENTIFIER":
                valor_ident_for = Parser.tokenizer.next.value
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "EQUAL":
                    Parser.tokenizer.selectNext()
                    init = Assignment("EQUAL", [Identifier(valor_ident_for, None), Parser.parseBoolExpression()])
                    if Parser.tokenizer.next.type == "SEMICOLON":
                        Parser.tokenizer.selectNext()
                        condition_for = Parser.parseBoolExpression()
                        if Parser.tokenizer.next.type == "SEMICOLON":
                            Parser.tokenizer.selectNext()
                            if Parser.tokenizer.next.type == "IDENTIFIER":
                                increment_ident_for = Parser.tokenizer.next.value
                                Parser.tokenizer.selectNext()
                                if Parser.tokenizer.next.type == "EQUAL":
                                    Parser.tokenizer.selectNext()
                                    increment = Assignment("EQUAL", [Identifier(increment_ident_for, None), Parser.parseBoolExpression()])
                                    block_for = Parser.parseBlock()
                                    resultado = For("FOR", [init, condition_for, increment, block_for])
                                    if Parser.tokenizer.next.type == "ENTER":
                                        Parser.tokenizer.selectNext()
                                        return resultado
                                    raise Exception("faltou Enter depois do for")
                                raise Exception("Faltou atribuir valor incremento do for")
                            raise Exception("Faltou incremento do for")
                        raise Exception("Faltou ponto e virgula depois do condition do for")
                    raise Exception("Faltou ponto e virgula depois do init do for")
                raise Exception("Nao atribuiu valor no init do for")
            raise Exception("Sem init do for")
        
        elif Parser.tokenizer.next.type == "VARIABLE":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "IDENTIFIER":
                valor_ident_var = Parser.tokenizer.next.value
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "INTTYPE" or Parser.tokenizer.next.type == "STRINGTYPE":
                    valor_type_var = Parser.tokenizer.next.value
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "EQUAL":
                        Parser.tokenizer.selectNext()
                        resultado = VarDec("VARIABLE", [valor_ident_var, valor_type_var, Parser.parseBoolExpression()])
                    else:
                        resultado = VarDec("VARIABLE", [valor_ident_var, valor_type_var, None])

                    if Parser.tokenizer.next.type == "ENTER":
                        Parser.tokenizer.selectNext()
                        return resultado
                    

        raise Exception("Nao usou uma funcionalidade") 
            

    def parseBlock():
        if Parser.tokenizer.next.type == "OPENKEY":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "ENTER":
                Parser.tokenizer.selectNext()
                resultado = Block(None, [])
                while Parser.tokenizer.next.type != "CLOSEKEY":
                    resultado.children.append(Parser.parseStatement())
                if Parser.tokenizer.next.type == "CLOSEKEY":
                    Parser.tokenizer.selectNext()
                    return resultado
                raise Exception("Nao fechou chaves")
            raise Exception("Nao deu enter depois de abrir chaves")
        raise Exception("Nao abriu chaves")

    def parseProgram():
        resultado = Block(None, [])
        while Parser.tokenizer.next.type != "EOF":
            resultado.children.append(Parser.parseStatement())
        return resultado

    
    def run(arquivo):
        ProCode = PrePro(arquivo, 0)
        texto = ProCode.filter()
        Parser.tokenizer.source = texto
        Parser.tokenizer.selectNext()
        resultado = Parser.parseProgram()
        if Parser.tokenizer.next.type != "EOF":
            raise Exception("Deveria ser o fim da string")
        return resultado
    
def main():
    Tabela = SymbolTable()
    arquivo = sys.argv[1]
    resultado = Parser.run(arquivo)
    resultado.Evaluate(Tabela)

if __name__ == "__main__":
    main()
            

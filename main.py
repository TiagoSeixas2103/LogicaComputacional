import sys

class Token:
    def __init__(self, type, value):
        self.type = str (type)
        self.value = None

class PrePro:
    def __init__(self, source, position):
        self.source = str (source)
        self.position = int (position)

    def filter(self):
        while self.position < len(self.source):
            if self.source[self.position] == "/" and self.source[self.position + 1] == "/":
                while self.position < len(self.source) and self.source[self.position] != "\n":
                    self.source = self.source[0:self.position]
            else:
                self.position += 1

class Tokenizer:
    def __init__(self, source, position, next):
        self.source = str (source)
        self.position = int (position)
        self.next = Token("", None)
        self.palavras_reservadas = {"Println" : "PRINT"}

    def selectNext(self):
        while self.position < len(self.source) and self.source[self.position] == " ":
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
            elif self.source[self.position] == "+":
                self.next.type = "PLUS"
                self.next.value = None
            elif self.source[self.position] == "-":
                self.next.type = "MINUS"
                self.next.value = None
            elif self.source[self.position] == "*":
                self.next.type = "MULT"
                self.next.value = None
            elif self.source[self.position] == "/":
                self.next.type = "DIV"
                self.next.value = None
            elif self.source[self.position] == "(":
                self.next.type = "OPENPAR"
                self.next.value = None
            elif self.source[self.position] == ")":
                self.next.type = "CLOSEPAR"
                self.next.value = None
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
                self.next.type = "EQUAL"
                self.next.value = None
            elif self.source[self.position] == "\n":
                self.next.type = "ENTER"
                self.next.value = None
            self.position += 1
        else:
            self.next.type = "EOF"
            self.next.value = None

class SymbolTable:
    def __init__(self):
        self.dicionario = {}

    def get_ST(self, id):
        if id in self.dicionario:
            return self.dicionario[id]
        else:
            raise Exception("Nao esta na Symbol Table")
    
    def set_ST(self, id, value):
        self.dicionario[id] = value

class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, SymbolTable):
        pass
    
class BinOp(Node):
    def Evaluate(self, SymbolTable):
        if self.value == "PLUS":  
            return self.children[0].Evaluate(SymbolTable) + self.children[1].Evaluate(SymbolTable)
        if self.value == "MINUS":   
            return self.children[0].Evaluate(SymbolTable) - self.children[1].Evaluate(SymbolTable)
        if self.value == "MULT":   
            return self.children[0].Evaluate(SymbolTable) * self.children[1].Evaluate(SymbolTable)
        if self.value == "DIV":   
            return self.children[0].Evaluate(SymbolTable) // self.children[1].Evaluate(SymbolTable)

class UnOp(Node):
    def Evaluate(self, SymbolTable):
        if self.value == "PLUS":   
            return self.children[0].Evaluate(SymbolTable)
        if self.value == "MINUS":   
            return -self.children[0].Evaluate(SymbolTable)

class IntVal(Node):
    def Evaluate(self, SymbolTable):
        return self.value

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
        print(self.children[0].Evaluate(SymbolTable)) 

class Parser:
    tokenizer = Tokenizer("", 0, Token("", None))
    def parseFactor():       
        if Parser.tokenizer.next.type == "INT":
            resultado = IntVal(Parser.tokenizer.next.value, None)
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
        elif Parser.tokenizer.next.type == "OPENPAR":
            Parser.tokenizer.selectNext()
            resultado = Parser.parseExpression()
            if Parser.tokenizer.next.type == "CLOSEPAR":
                Parser.tokenizer.selectNext()
                return resultado
            raise Exception("Nao fechou parenteses")
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
        while Parser.tokenizer.next.type == "PLUS" or Parser.tokenizer.next.type == "MINUS":
            if Parser.tokenizer.next.type == "PLUS":
                Parser.tokenizer.selectNext()
                resultado = BinOp("PLUS",[resultado, Parser.parseTerm()])
            if Parser.tokenizer.next.type == "MINUS":
                Parser.tokenizer.selectNext()
                resultado = BinOp("MINUS",[resultado, Parser.parseTerm()])
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
                resultado = Assignment("EQUAL", [Identifier(valor_ident, None), Parser.parseExpression()])
                if Parser.tokenizer.next.type == "ENTER":
                    Parser.tokenizer.selectNext()
                    return resultado
                raise Exception("Nao deu Enter 1")
            raise Exception("Nao botou igual ou sinal")
        
        elif Parser.tokenizer.next.type == "PRINT":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "OPENPAR":
                Parser.tokenizer.selectNext()
                resultado = Println("PRINT", [Parser.parseExpression()])
                if Parser.tokenizer.next.type == "CLOSEPAR":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "ENTER":
                        Parser.tokenizer.selectNext()
                        return resultado
                    raise Exception("Nao deu Enter 2")
                raise Exception("Nao fechou parenteses")
            raise Exception("Nao abriu parenteses")
        raise Exception("Nao usou uma funcionalidade")        


    def parseBlock():
        resultado = Block(None, [])
        while Parser.tokenizer.next.type != "EOF":
            resultado.children.append(Parser.parseStatement())
        return resultado

    
    def run(code):
        ProCode = PrePro(code, 0)
        ProCode.filter()
        Parser.tokenizer.source = ProCode.source
        Parser.tokenizer.selectNext()
        resultado = Parser.parseBlock()
        if Parser.tokenizer.next.type != "EOF":
            raise Exception("Deveria ser o fim da string")
        return resultado
    
def main():
    Tabela = SymbolTable()
    arquivo = open(sys.argv[1])
    resultado = Parser.run(arquivo.read())
    resultado.Evaluate(Tabela)

if __name__ == "__main__":
    main()
            

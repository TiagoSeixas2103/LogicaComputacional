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
            self.position += 1
        else:
            self.next.type = "EOF"
            self.next.value = None

class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self):
        pass
    
class BinOp(Node):
    def Evaluate(self):
        if self.value == "PLUS":   
            return self.children[0].Evaluate() + self.children[1].Evaluate()
        if self.value == "MINUS":   
            return self.children[0].Evaluate() - self.children[1].Evaluate()
        if self.value == "MULT":   
            return self.children[0].Evaluate() * self.children[1].Evaluate()
        if self.value == "DIV":   
            return self.children[0].Evaluate() // self.children[1].Evaluate()

class UnOp(Node):
    def Evaluate(self):
        if self.value == "PLUS":   
            return self.children[0].Evaluate()
        if self.value == "MINUS":   
            return -self.children[0].Evaluate()

class IntVal(Node):
    def Evaluate(self):
        return self.value

class NoOp(Node):
    def Evaluate(self):
        pass
        

class Parser:
    tokenizer = Tokenizer("", 0, Token("", None))
    def parseFactor():        
        if Parser.tokenizer.next.value != None:
            resultado = IntVal(Parser.tokenizer.next.value, None)
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

    
    def run(code):
        ProCode = PrePro(code, 0)
        ProCode.filter()
        Parser.tokenizer.source = ProCode.source
        Parser.tokenizer.selectNext()
        resultado = Parser.parseExpression()
        if Parser.tokenizer.next.type != "EOF":
            raise Exception("Deveria ser o fim da string")
        return resultado
    
def main():
    arquivo = open(sys.argv[1])
    resultado = Parser.run(arquivo.read())
    print(resultado.Evaluate())

if __name__ == "__main__":
    main()
            

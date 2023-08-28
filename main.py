import sys

class Token:
    def __init__(self, type, value):
        self.type = str (type)
        self.value = None

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
            self.position += 1
        else:
            self.next.type = "EOF"
            self.next.value = None


class Parser:
    tokenizer = Tokenizer("", 0, Token("", None))
    def parseTerm():
        if Parser.tokenizer.next.value != None:
            num = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            while Parser.tokenizer.next.type == "MULT" or Parser.tokenizer.next.type == "DIV":
                if Parser.tokenizer.next.type == "MULT":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.value != None:
                        num *= Parser.tokenizer.next.value
                    else:
                        raise Exception("Um numero deveria seguir token MULT")
                if Parser.tokenizer.next.type == "DIV":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.value != None:
                        num = num // Parser.tokenizer.next.value
                    else:
                        raise Exception("Um numero deveria seguir token DIV")
                Parser.tokenizer.selectNext()
            return num
        raise Exception("Primeiro token nao eh numero")

    def parseExpression():
        while Parser.tokenizer.next.value != None:
            resultado = Parser.parseTerm()        
            if Parser.tokenizer.next.type == "PLUS":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.value != None:
                    resultado += Parser.tokenizer.next.value
                else:
                    raise Exception("Um numero deveria seguir token PLUS")
            if Parser.tokenizer.next.type == "MINUS":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.value != None:
                    resultado -= Parser.tokenizer.next.value
                else:
                    raise Exception("Um numero deveria seguir token MINUS")
            Parser.tokenizer.selectNext()
        return resultado


    
    def run(code):
        Parser.tokenizer.source = code
        Parser.tokenizer.selectNext()
        resultado = Parser.parseExpression()
        if Parser.tokenizer.next.type != "EOF":
            raise Exception("Deveria ser o fim da string")
        return resultado
    
def main():
    resultado = Parser.run(sys.argv[1])
    print(resultado)

if __name__ == "__main__":
    main()
            

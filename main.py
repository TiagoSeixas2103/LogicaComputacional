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
            self.position += 1
        else:
            self.next.type = "EOF"
            self.next.value = None


class Parser:
    tokenizer = Tokenizer("", 0, Token("", None))
    def parseExpression():
        if Parser.tokenizer.next.value != None:
            resultado = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            while Parser.tokenizer.next.type == "PLUS" or Parser.tokenizer.next.type == "MINUS":
                if Parser.tokenizer.next.type == "PLUS":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.value != None:
                        resultado += Parser.tokenizer.next.value
                    else:
                        raise Exception("ERRO")
                if Parser.tokenizer.next.type == "MINUS":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.value != None:
                        resultado -= Parser.tokenizer.next.value
                    else:
                        raise Exception("ERRO")
                Parser.tokenizer.selectNext()
            return resultado
        raise Exception("ERRO")
    
    def run(code):
        Parser.tokenizer.source = code
        Parser.tokenizer.selectNext()
        resultado = Parser.parseExpression()
        if Parser.tokenizer.next.type != "EOF":
            raise Exception("ERRO")
        return resultado
    
def main():
    resultado = Parser.run(sys.argv[1])
    print(resultado)

if __name__ == "__main__":
    main()
            

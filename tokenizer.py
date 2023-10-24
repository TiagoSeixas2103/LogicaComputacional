class Token:
    def __init__(self, type, value):
        self.type = str (type)
        self.value = None

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
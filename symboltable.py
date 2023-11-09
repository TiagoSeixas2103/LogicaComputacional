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
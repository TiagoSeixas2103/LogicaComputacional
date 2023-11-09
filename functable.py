class FuncTable:
    def __init__(self):
        self.dicionario = {}
        self.type = {}

    def get_ST(self, id):
        if id in self.dicionario and id in self.type:
            return (self.dicionario[id], self.type[id])
        else:
            raise Exception("Nao esta na Func Table")

    def set_ST(self, id, value):
        if id in self.type and id in self.dicionario:
            self.dicionario[id] = value
        else:
            raise Exception("Funcao nao declarada")

    def create_ST(self, id, type, value):
        if id not in self.dicionario:
            self.dicionario[id] = value
            self.type[id] = type
        else:
            raise Exception("Funcao ja declarada")
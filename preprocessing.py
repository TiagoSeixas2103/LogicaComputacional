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
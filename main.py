import sys

apareceu_numero = 0
repete_simbolo = 0
numero = 0
simbolo = ""
contagem = 0
valor = 0

for elemento in sys.argv[1]:
    if elemento.isdigit() and not contagem:
        repete_simbolo = 0
        apareceu_numero = 1
        contagem = 1

    if elemento.isdigit():
        repete_simbolo = 0
        if simbolo == "-":
            valor += numero
        else:
            valor -= numero
        numero = numero * 10
        numero += int(elemento)

        if simbolo == "-":
            valor -= numero
        else:
            valor += numero

    else:
        if (elemento == "+" or elemento == "-") and apareceu_numero and elemento != "'":
            if repete_simbolo == 1:
                raise Exception('Simbolos consecutivos')
            simbolo = elemento
            numero = 0
            repete_simbolo = 1
        elif (elemento == "+" or elemento == "-") and (not apareceu_numero or contagem == 0):
            raise Exception('Nao teve numero precedendo simbolo, ou foi string vazia')

if repete_simbolo == 1:
    raise Exception('Terminou em simbolo')

print(valor)
import sys

valor = 0
confirma_nulo = 0
numero = 0
simbolo = ""

if sys.argv[1] == "''":
    confirma_nulo = 1

for i in range(len(sys.argv[1])):
    if sys.argv[1][i].isdigit():
        if simbolo == "-":
            valor += numero
        else:
            valor -= numero
        numero = numero * 10
        numero += int(sys.argv[1][i])
        print(numero)
        
        if simbolo == "-":
            valor -= numero
        else:
            valor += numero

    else:
        if sys.argv[1][i] != "+" or sys.argv[1][i] != "-":
            simbolo = sys.argv[1][i]
            numero = 0

if not (confirma_nulo):
    print(valor)
import sys

apareceu_numero = 0
numero = 0
simbolo = ""
contagem = 0

for elemento in sys.argv[1]:
    if elemento.isdigit() and not contagem:
        apareceu_numero = 1
        contagem = 1
        valor = 0

    if elemento.isdigit():
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
        if (elemento == "+" or elemento == "-") and apareceu_numero:
            simbolo = elemento
            numero = 0
        elif (elemento == "+" or elemento == "-") and (not apareceu_numero or contagem == 0):
            valor = "erro"
            break

print(valor)
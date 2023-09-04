# Status dos testes
![git status](http://3.129.230.99/svg/TiagoSeixas2103/LogicaComputacional/)

# Diagrama Sintatico
![alt text](img/diagramaSintatico.png)

# EBNF
```c
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = ("+" | "-") FACTOR | "(" EXPRESSION ")" | number ;
```

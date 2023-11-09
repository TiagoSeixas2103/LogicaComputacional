import sys
from parsergo import Parser
from symboltable import SymbolTable
from functable import FuncTable
    
def main():
    Tabela = SymbolTable()
    TabelaFunc = FuncTable()
    arquivo = sys.argv[1]
    resultado = Parser.run(arquivo)
    resultado.Evaluate(Tabela, TabelaFunc)

if __name__ == "__main__":
    main()
            

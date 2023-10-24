import sys
from parsergo import Parser
from symboltable import SymbolTable
    
def main():
    Tabela = SymbolTable()
    arquivo = sys.argv[1]
    resultado = Parser.run(arquivo)
    resultado.Evaluate(Tabela)

if __name__ == "__main__":
    main()
            

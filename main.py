import sys
from parsergo import Parser
from symboltable import SymbolTable
from initasm import InitializeASM
from endasm import FinalizeASM
    
def main():
    InitializeASM.writeInitASM()
    Tabela = SymbolTable()
    arquivo = sys.argv[1]
    resultado = Parser.run(arquivo)
    resultado.Evaluate(Tabela)
    FinalizeASM.writeEndASM()

if __name__ == "__main__":
    main()
            

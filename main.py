import sys
from parsergo import Parser
from symboltable import SymbolTable
from initasm import InitializeASM
from endasm import FinalizeASM
from write import WriteASM
    
def main():
    Tabela = SymbolTable()
    arquivo = sys.argv[1]
    arquivoASM = sys.argv[2]
    InitializeASM.writeInitASM(arquivoASM)
    WriteASM.program = arquivoASM
    resultado = Parser.run(arquivo)
    resultado.Evaluate(Tabela)
    FinalizeASM.writeEndASM(arquivoASM)

if __name__ == "__main__":
    main()
            

from tokenizer import Token, Tokenizer
from preprocessing import PrePro
from nodeclasses import BinOp, UnOp, IntVal, StrVal, VarDec, NoOp
from nodeclasses import Identifier, Assignment, Block, Println, If, For

class Parser:
    tokenizer = Tokenizer("", 0, Token("", None))
    def parseFactor():       
        if Parser.tokenizer.next.type == "INT":
            resultado = IntVal(Parser.tokenizer.next.value, None)
            Parser.tokenizer.selectNext()
            return resultado
        if Parser.tokenizer.next.type == "STRING":
            resultado = StrVal(Parser.tokenizer.next.value, None)
            Parser.tokenizer.selectNext()
            return resultado
        elif Parser.tokenizer.next.type == "IDENTIFIER":
            resultado = Identifier(Parser.tokenizer.next.value, None)
            Parser.tokenizer.selectNext()
            return resultado
        elif Parser.tokenizer.next.type == "PLUS":
            Parser.tokenizer.selectNext()
            resultado = UnOp("PLUS", [Parser.parseFactor()])
            return resultado
        elif Parser.tokenizer.next.type == "MINUS":
            Parser.tokenizer.selectNext()
            resultado = UnOp("MINUS", [Parser.parseFactor()])
            return resultado
        elif Parser.tokenizer.next.type == "NOT":
            Parser.tokenizer.selectNext()
            resultado = UnOp("NOT", [Parser.parseFactor()])
            return resultado
        elif Parser.tokenizer.next.type == "OPENPAR":
            Parser.tokenizer.selectNext()
            resultado = Parser.parseBoolExpression()
            if Parser.tokenizer.next.type == "CLOSEPAR":
                Parser.tokenizer.selectNext()
                return resultado
            raise Exception("Nao fechou parenteses")
        elif Parser.tokenizer.next.type == "SCAN":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "OPENPAR":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "CLOSEPAR":
                    Parser.tokenizer.selectNext()
                    #resultado = IntVal(int(input()), ["scan"])
                    resultado = IntVal(0, ["scan"])
                    return resultado
                raise Exception("Nao fechou parenteses no scan")
            raise Exception("Nao abriu parenteses no scan")
        else:
           raise Exception("Nao foi factor") 

    def parseTerm():
        resultado = Parser.parseFactor() 
        while Parser.tokenizer.next.type == "MULT" or Parser.tokenizer.next.type == "DIV":
            if Parser.tokenizer.next.type == "MULT":
                Parser.tokenizer.selectNext()
                resultado  = BinOp("MULT",[resultado, Parser.parseFactor()])
            if Parser.tokenizer.next.type == "DIV":
                Parser.tokenizer.selectNext()
                resultado  = BinOp("DIV",[resultado, Parser.parseFactor()])
        return resultado

    def parseExpression():
        resultado = Parser.parseTerm() 
        dict = {
            "PLUS" : "PLUS",
            "MINUS" : "MINUS",
            "DOT" : "DOT",
            }
        while Parser.tokenizer.next.type in dict:
            if Parser.tokenizer.next.type == "PLUS":
                Parser.tokenizer.selectNext()
                resultado = BinOp("PLUS",[resultado, Parser.parseTerm()])
            if Parser.tokenizer.next.type == "MINUS":
                Parser.tokenizer.selectNext()
                resultado = BinOp("MINUS",[resultado, Parser.parseTerm()])
            if Parser.tokenizer.next.type == "DOT":
                Parser.tokenizer.selectNext()
                resultado = BinOp("DOT",[resultado, Parser.parseTerm()])
        return resultado
    
    def parseRelationalExpression():
        resultado = Parser.parseExpression()
        condicao = Parser.tokenizer.next.type 
        while condicao == "EQUALTO" or condicao == "GREATERTHAN" or condicao == "LOWERTHAN":
            if Parser.tokenizer.next.type == "EQUALTO":
                Parser.tokenizer.selectNext()
                resultado = BinOp("EQUALTO",[resultado, Parser.parseExpression()])
            if Parser.tokenizer.next.type == "GREATERTHAN":
                Parser.tokenizer.selectNext()
                resultado = BinOp("GREATERTHAN",[resultado, Parser.parseExpression()])
            if Parser.tokenizer.next.type == "LOWERTHAN":
                Parser.tokenizer.selectNext()
                resultado = BinOp("LOWERTHAN",[resultado, Parser.parseExpression()])
            condicao = Parser.tokenizer.next.type
        return resultado

    def parseBoolTerm():
        resultado = Parser.parseRelationalExpression() 
        while Parser.tokenizer.next.type == "AND":
            Parser.tokenizer.selectNext()
            resultado = BinOp("AND",[resultado, Parser.parseRelationalExpression()])
        return resultado
    
    def parseBoolExpression():
        resultado = Parser.parseBoolTerm() 
        while Parser.tokenizer.next.type == "OR":
            Parser.tokenizer.selectNext()
            resultado = BinOp("OR",[resultado, Parser.parseBoolTerm()])
        return resultado
    
    def parseStatement():
        resultado = NoOp(None, [])
        if Parser.tokenizer.next.type == "ENTER":
            Parser.tokenizer.selectNext()
            return resultado
        
        elif Parser.tokenizer.next.type == "IDENTIFIER":
            valor_ident = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "EQUAL":
                Parser.tokenizer.selectNext()
                resultado = Assignment("EQUAL", [Identifier(valor_ident, None), Parser.parseBoolExpression()])
                if Parser.tokenizer.next.type == "ENTER":
                    Parser.tokenizer.selectNext()
                    return resultado
                raise Exception("Nao deu Enter depois do assignment")
            raise Exception("Nao botou igual ou sinal")
        
        elif Parser.tokenizer.next.type == "PRINT":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "OPENPAR":
                Parser.tokenizer.selectNext()
                resultado = Println("PRINT", [Parser.parseBoolExpression()])
                if Parser.tokenizer.next.type == "CLOSEPAR":
                    Parser.tokenizer.selectNext()
                    return resultado
                raise Exception("Nao fechou parenteses")
            raise Exception("Nao abriu parenteses")
        
        elif Parser.tokenizer.next.type == "IF":
            Parser.tokenizer.selectNext()
            condition = Parser.parseBoolExpression()
            block = Parser.parseBlock()
            resultado = If("IF", [condition, block])
            if Parser.tokenizer.next.type == "ELSE":
                Parser.tokenizer.selectNext()
                newBlock = Parser.parseBlock()
                resultado.children.append(newBlock)
            if Parser.tokenizer.next.type == "ENTER":
                Parser.tokenizer.selectNext()
                return resultado
            raise Exception("faltou Enter depois do if")
        
        elif Parser.tokenizer.next.type == "FOR":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "IDENTIFIER":
                valor_ident_for = Parser.tokenizer.next.value
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "EQUAL":
                    Parser.tokenizer.selectNext()
                    init = Assignment("EQUAL", [Identifier(valor_ident_for, None), Parser.parseBoolExpression()])
                    if Parser.tokenizer.next.type == "SEMICOLON":
                        Parser.tokenizer.selectNext()
                        condition_for = Parser.parseBoolExpression()
                        if Parser.tokenizer.next.type == "SEMICOLON":
                            Parser.tokenizer.selectNext()
                            if Parser.tokenizer.next.type == "IDENTIFIER":
                                increment_ident_for = Parser.tokenizer.next.value
                                Parser.tokenizer.selectNext()
                                if Parser.tokenizer.next.type == "EQUAL":
                                    Parser.tokenizer.selectNext()
                                    increment = Assignment("EQUAL", [Identifier(increment_ident_for, None), Parser.parseBoolExpression()])
                                    block_for = Parser.parseBlock()
                                    resultado = For("FOR", [init, condition_for, increment, block_for])
                                    if Parser.tokenizer.next.type == "ENTER":
                                        Parser.tokenizer.selectNext()
                                        return resultado
                                    raise Exception("faltou Enter depois do for")
                                raise Exception("Faltou atribuir valor incremento do for")
                            raise Exception("Faltou incremento do for")
                        raise Exception("Faltou ponto e virgula depois do condition do for")
                    raise Exception("Faltou ponto e virgula depois do init do for")
                raise Exception("Nao atribuiu valor no init do for")
            raise Exception("Sem init do for")
        
        elif Parser.tokenizer.next.type == "VARIABLE":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "IDENTIFIER":
                valor_ident_var = Parser.tokenizer.next.value
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "INTTYPE" or Parser.tokenizer.next.type == "STRINGTYPE":
                    valor_type_var = Parser.tokenizer.next.value
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "EQUAL":
                        Parser.tokenizer.selectNext()
                        resultado = VarDec("VARIABLE", [valor_ident_var, valor_type_var, Parser.parseBoolExpression()])
                    else:
                        resultado = VarDec("VARIABLE", [valor_ident_var, valor_type_var, None])

                    if Parser.tokenizer.next.type == "ENTER":
                        Parser.tokenizer.selectNext()
                        return resultado
                    

        raise Exception("Nao usou uma funcionalidade") 
            

    def parseBlock():
        if Parser.tokenizer.next.type == "OPENKEY":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "ENTER":
                Parser.tokenizer.selectNext()
                resultado = Block(None, [])
                while Parser.tokenizer.next.type != "CLOSEKEY":
                    resultado.children.append(Parser.parseStatement())
                if Parser.tokenizer.next.type == "CLOSEKEY":
                    Parser.tokenizer.selectNext()
                    return resultado
                raise Exception("Nao fechou chaves")
            raise Exception("Nao deu enter depois de abrir chaves")
        raise Exception("Nao abriu chaves")

    def parseProgram():
        resultado = Block(None, [])
        while Parser.tokenizer.next.type != "EOF":
            resultado.children.append(Parser.parseStatement())
        return resultado

    
    def run(arquivo):
        ProCode = PrePro(arquivo, 0)
        texto = ProCode.filter()
        Parser.tokenizer.source = texto
        Parser.tokenizer.selectNext()
        resultado = Parser.parseProgram()
        if Parser.tokenizer.next.type != "EOF":
            raise Exception("Deveria ser o fim da string")
        return resultado
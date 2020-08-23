from lexer import generate
from ox_parser import Parser
from ox_parsers import genAST

def shell():
    while True:
        text = input('oxide> ')
        if text == '.exit':
            break
        tokens = generate('<stdin>', text)
        if tokens[1]:
            print(tokens[1])
            continue
        parser = Parser(tokens[0], genAST)
        ast = parser.gen_ast()
        if ast.error:
            print(ast.error)
            continue
        print(ast.node)

if __name__ == "__main__":
    shell()
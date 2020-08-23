from lexer import generate
from ox_parser import Parser
from ox_parsers import genAST
from interpreter import Context
from utils import NodeList

def shell_tree(ast, ctx):
    if isinstance(ast, NodeList):
        for node in ast:
            shell_tree(node, ctx)
        return
    value = ast.visit(ctx)
    if value.error: return print(value.error)
    print(value.value)

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
        base_context = Context('<stdin>')
        shell_tree(ast.node, base_context)

if __name__ == "__main__":
    shell()
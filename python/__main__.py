from lexer import generate
from ox_parser import Parser
from ox_parsers import genAST
from interpreter import Context
from utils import NodeList
from symbol_table import SymbolTable
import os

def shell_tree(ast, ctx):
    if isinstance(ast, NodeList):
        for node in ast:
            shell_tree(node, ctx)
        return
    value = ast.visit(ctx)
    if value.error: return print(value.error)
    print('<·', value.value)

def shell():
    base_context = Context('<stdin>')
    base_symbol_table = SymbolTable()
    base_context.symbol_table = base_symbol_table
    while True:
        text = input('oxide> ')
        if text == '.exit':
            break
        if text == '.clear':
            os.system('cls' if os.name == 'nt' else 'clear')
            continue
        tokens = generate('<stdin>', text)
        if tokens[1]:
            print(tokens[1])
            continue
        parser = Parser(tokens[0], genAST)
        ast = parser.gen_ast()
        if ast.error:
            print(ast.error)
            continue
        shell_tree(ast.node, base_context)

if __name__ == "__main__":
    shell()
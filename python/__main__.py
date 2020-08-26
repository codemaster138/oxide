from lexer import generate
from ox_parser import Parser
from ox_parsers import genAST
from interpreter import Context
from utils import NodeList
from symbol_table import SymbolTable
import os
import sys
import os.path

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
        text = None
        try:
            text = input('oxide> ')
        except KeyboardInterrupt:
            print()
            break
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

def file_tree(ast , ctx):
    if isinstance(ast, NodeList):
        for node in ast:
            file_tree(node, ctx)
        return
    value = ast.visit(ctx)
    if value.error: return print(value.error)


def runFile(fl):
    if not os.path.isfile(fl):
        print('Error: \x1b[31;1mFileError\x1b[0m: File not found')
    with open(fl) as file:
        base_context = Context(fl)
        base_symbols = SymbolTable()
        base_context.symbol_table = base_symbols
        tokens = generate(fl, file.read())
        if tokens[1]:
            print(tokens[1])
            return
        parser = Parser(tokens[0], genAST)
        ast = parser.gen_ast()
        if ast.error:
            print(ast.error)
            return
        file_tree(ast.node, base_context)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        runFile(sys.argv[1])
    else:
        shell()
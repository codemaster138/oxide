from nodes import *
from utils import NodeList
from ox_parser import ParseResult
from errors import InvalidTokenError, ExpectedTokenError

def genAST(parser):
    res = ParseResult()
    nodes = res.register(adjancentNodes(parser, 'EOF'))
    if res.error: return res
    return res.success(nodes)

def adjancentNodes(parser, end):
    res = ParseResult()
    nodes = NodeList()
    while not parser.cur_token == end or parser.cur_token == None:
        node = res.register(expr(parser))
        if res.error: return res
        nodes.append(node)
        if parser.cur_token == 'SEMICOLON':
            parser.advance()
    parser.advance()
    return res.success(nodes)

def expr(parser):
    res = ParseResult()
    node = res.register(bin_op(parser, ('AND', 'OR'), compexpr))
    if res.error: return res
    return res.success(node)

def compexpr(parser):
    res = ParseResult()
    if parser.cur_token == 'NOT':
        op_tok = parser.cur_token
        parser.advance()
        node = res.register(compexpr(parser))
        if res.error: return res
        return res.success(UnaryOpNode(op_tok, node))
    node = res.register(bin_op(parser, ('EE', 'LT', 'GT', 'LTE', 'GTE', 'NE'), arithexpr))
    if res.error: return res
    return res.success(node)

def arithexpr(parser):
    res = ParseResult()
    node = res.register(bin_op(parser, ('PLUS', 'MINUS'), term))
    if res.error: return res
    return res.success(node)

def term(parser):
    res = ParseResult()
    node = res.register(bin_op(parser, ('MUL', 'DIV'), factor))
    if res.error: return res
    return res.success(node)

def factor(parser):
    res = ParseResult()
    if parser.cur_token.type in ('PLUS', 'MINUS'):
        op_tok = parser.cur_token
        parser.advance()
        node = res.register(factor(parser))
        if res.error: return res
        return res.success(UnaryOpNode(op_tok, node))
    node = res.register(power(parser))
    if res.error: return res
    return res.success(node)

def power(parser):
    res = ParseResult()
    node = res.register(bin_op(parser, ('POW', 'NPOW'), atom))
    if res.error: return res
    return res.success(node)

def atom(parser):
    res = ParseResult()
    if parser.cur_token.type in ('INT', 'FLOAT'):
        token = parser.cur_token
        parser.advance()
        node = NumberNode(token)
        return res.success(node)
    if parser.cur_token.type in ('TRUE', 'FALSE'):
        token = parser.cur_token
        parser.advance()
        node = BooleanNode(token)
        return res.success(node)
    if parser.cur_token == 'KEYWORD':
        if parser.cur_token > "if":
            node = res.register(if_expr(parser))
            if res.error: return res
            return res.success(node)
    if parser.cur_token == 'LPAREN':
        parser.advance()
        expr_ = res.register(expr(parser))
        if res.error: return res
        if not parser.cur_token == 'RPAREN':
            return res.failure(ExpectedTokenError(')', parser.cur_token.pos_start))
        parser.advance()
        return res.success(expr_)
    if parser.cur_token == "LBRACK":
        node = res.register(list_expr(parser))
        if res.error: return res
        return res.success(node)
    return res.failure(InvalidTokenError(parser.cur_token))

def bin_op(parser, ops, leftFn, rightFn=None):
    if rightFn == None:
        rightFn = leftFn
    res = ParseResult()
    left = res.register(leftFn(parser))
    if res.error: return res
    while parser.cur_token.type in ops:
        op_tok = parser.cur_token
        parser.advance()
        right = res.register(rightFn(parser))
        if res.error: return res
        left = BinOpNode(left, op_tok, right)
    return res.success(left)

def if_expr(parser):
    res = ParseResult()
    if not (parser.cur_token == 'KEYWORD' and parser.cur_token > "if"):
        return res.failure(ExpectedTokenError('if', parser.cur_token.pos_start))
    parser.advance()
    comp = res.register(expr(parser))
    if res.error: return res
    if parser.cur_token == 'LCURL':
        parser.advance()
        bodyNodes = res.register(adjancentNodes(parser, 'RCURL'))
        if res.error: return res
        node = IfNode(comp, bodyNodes)
        return res.success(node)
    else:
        body = res.register(expr(parser))
        if res.error: return res
        bodyNodes = NodeList(body)
        node = IfNode(comp, bodyNodes)
        return res.success(node)

def list_expr(parser):
    res = ParseResult()
    if not parser.cur_token == 'LBRACK':
        return res.failure(ExpectedTokenError('[', parser.cur_token.pos_start))
    parser.advance()
    if parser.cur_token == 'RBRACK':
        # Empty array
        parser.advance()
        node = ArrayNode()
        return res.success(node)
    first_node = res.register(expr(parser))
    if res.error: return res
    if parser.cur_token == 'RBRACK':
        parser.advance()
        node = ArrayNode([first_node])
        return res.success(node)
    if not parser.cur_token == 'COMMA':
        return res.failure(ExpectedTokenError(',', parser.cur_token.pos_start))
    contents = [first_node]
    while parser.cur_token == 'COMMA':
        parser.advance()
        content_node = res.register(expr(parser))
        if res.error: return res
        contents.append(content_node)
    if parser.cur_token == 'RBRACK':
        parser.advance()
        node = ArrayNode(contents)
        return res.success(node)
    else:
        return res.failure(ExpectedTokenError(']', parser.cur_token.pos_start))
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
    return res.success(nodes)

def expr(parser):
    res = ParseResult()
    node = res.register(bin_op(parser, ('PLUS', 'MINUS'), term))
    if res.error: return res
    return res.success(node)

def term(parser):
    res = ParseResult()
    node = res.register(bin_op(parser, ('MUL', 'DIV'), power))
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
    if parser.cur_token == 'LPAREN':
        parser.advance()
        expr_ = res.register(expr(parser))
        if res.error: return res
        if not parser.cur_token == 'RPAREN':
            return res.failure(ExpectedTokenError(')', parser.cur_token.pos_start))
        parser.advance()
        return res.success(expr_)
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
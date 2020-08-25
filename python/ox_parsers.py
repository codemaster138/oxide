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
    if parser.cur_token == 'KEYWORD':
        if parser.cur_token > 'var':
            parser.advance()
            if parser.cur_token != 'IDENTIFIER':
                return res.failure(ExpectedTokenError('identifier', parser.cur_token.pos_start))
            name_tok = parser.cur_token
            parser.advance()
            if parser.cur_token != 'EQ':
                return res.failure(ExpectedTokenError('=', parser.cur_token.pos_start))
            parser.advance()
            value_node = res.register(expr(parser))
            if res.error: return res
            node = VarCreateNode(name_tok, value_node)
            return res.success(node)
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
    if parser.cur_token.type == 'UNDEF':
        node = UndefNode(parser.cur_token)
        parser.advance()
        return res.success(node)
    if parser.cur_token.type == 'IDENTIFIER':
        name_tok = parser.cur_token
        parser.advance()
        if parser.cur_token.type == 'EQ':
            parser.advance()
            value_node = res.register(expr(parser))
            if res.error: return res
            node = VarAssignNode(name_tok, value_node)
            return res.success(node)
        node = VarAccessNode(name_tok)
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
        if parser.cur_token > "func":
            node = res.register(func_def(parser))
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
    bodyNodes = None
    if res.error: return res
    if parser.cur_token == 'LCURL':
        bodyNodes = res.register(block(parser))
        if res.error: return res
        #node = IfNode(comp, bodyNodes)
        #return res.success(node)
    else:
        body = res.register(expr(parser))
        if res.error: return res
        bodyNodes = NodeList(body)
        #node = IfNode(comp, bodyNodes)
        #return res.success(node)
    elseNodes = None
    if (parser.cur_token == 'KEYWORD' and parser.cur_token > "else"):
        parser.advance()
        if parser.cur_token == 'LCURL':
            elseNodes = res.register(block(parser))
            if res.error: return res
            #node = IfNode(comp, bodyNodes)
            #return res.success(node)
        else:
            elseNode = res.register(expr(parser))
            if res.error: return res
            elseNodes = NodeList(elseNode)
            #node = IfNode(comp, bodyNodes)
            #return res.success(node)
    if elseNodes == None:
        node = IfNode(comp, bodyNodes, NodeList())
        return res.success(node)
    node = IfNode(comp, bodyNodes, elseNodes)
    return res.success(node)

def block(parser):
    res = ParseResult()
    if parser.cur_token.type != 'LCURL':
        return ExpectedTokenError('{', parser.cur_toke.pos_start)
    parser.advance()
    bodyNodes = res.register(adjancentNodes(parser, 'RCURL'))
    if res.error: return res
    return res.success(bodyNodes)

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

def func_def(parser):
    res = ParseResult()
    if not parser.cur_token < 'KEYWORD:func': return res.failure(ExpectedTokenError('func', parser.cur_token.pos_start))
    start = parser.cur_token.pos_start
    parser.advance()
    if not parser.cur_token == 'IDENTIFIER': return res.failure(ExpectedTokenError('identifier', parser.cur_token.pos_start))
    name_tok = parser.cur_token
    parser.advance()
    if not parser.cur_token == 'LPAREN': return res.failure(ExpectedTokenError('`(`', parser.cur_token.pos_start))
    parser.advance()
    arg_toks = []
    if parser.cur_token == 'RPAREN':
        parser.advance()
    else:
        if not parser.cur_token == 'IDENTIFIER': res.failure(ExpectedTokenError('identifier', parser.cur_token.pos_start))
        arg_toks.append(parser.cur_token)
        parser.advance()
        while parser.cur_token == 'COMMA':
            parser.advance()
            if not parser.cur_token == 'IDENTIFIER': res.failure(ExpectedTokenError('identifier', parser.cur_token.pos_start))
            arg_toks.append(parser.cur_token)
            parser.advance()
        if not parser.cur_token == 'RPAREN': return res.failure(ExpectedTokenError('`)`', parser.cur_token.pos_start))
        parser.advance()
        body = res.register(block(parser))
        if res.error: return res
        return res.success(FunctionNode(arg_toks, body, start, parser.cur_token.pos_start))
from utils import Node
from interpreter import RTResult
from values import *
from errors import AssignmentException, OperationError

################################
#             NODES            #
################################
# This file defines all nodes created by the parser

class NumberNode(Node):
    def __init__(self, value_tok):
        self.value_tok = value_tok
        self.pos_start = value_tok.pos_start
        self.pos_end = value_tok.pos_end
    
    def __repr__(self):
        return str(self.value_tok.value)
    
    def visit(self, context):
        res = RTResult()
        v = Number.before(self.value_tok.value)
        if v:
            return res.success(Number(v))
        return res.failure(AssignmentException(self.value_tok, 'Number', ctx))

class BinOpNode(Node):
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        self.pos_start = left_node.pos_start
        self.pos_end = right_node.pos_end
    
    def __repr__(self):
        return f'({self.left_node} {self.op_tok.value} {self.right_node})'
    
    def visit(self, context):
        res = RTResult()
        left = res.register(self.left_node.visit(context))
        if res.error: return res
        right = res.register(self.right_node.visit(context))
        if res.error: return res
        operations = {
            "PLUS": 'add',
            'MINUS': 'sub',
            'MUL': 'mul',
            'DIV': 'div',
            'POW': 'pow',
            'NPOW': 'npow'
        }
        op = operations.get(self.op_tok.type)
        if not op:
            return res.failure(OperationError(self.op_tok, type(left).__name__, 'No such operator', context))
        result = left.operation(op, right)
        if result[1]:
            return res.failure(OperationError(self.op_tok, type(left).__name__, result[1], context))
        return res.success(result[0])
from utils import Node

################################
#             NODES            #
################################
# This file defines all nodes created by the parser

class PrimitiveNode(Node):
    def __init__(self, value_tok):
        self.value_tok = value_tok
        self.pos_start = value_tok.pos_start
        self.pos_end = value_tok.pos_end
    
    def __repr__(self):
        return str(self.value_tok.value)

class BinOpNode(Node):
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        self.pos_start = left_node.pos_start
        self.pos_end = right_node.pos_end
    
    def __repr__(self):
        return f'({self.left_node} {self.op_tok.value} {self.right_node})'
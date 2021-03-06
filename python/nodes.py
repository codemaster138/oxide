from utils import Node, NodeList
from interpreter import RTResult
from values import *
from errors import *
from token import Token

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
    
    def visit(self, ctx):
        res = RTResult()
        v = Number.before(self.value_tok.value)
        if v:
            return res.success(Number(v))
        return res.failure(AssignmentException(self.value_tok, 'Number', ctx))

class BooleanNode(Node):
    def __init__(self, value_tok):
        self.value_tok = value_tok
        self.pos_start = value_tok.pos_start
        self.pos_end = value_tok.pos_end
    
    def __repr__(self):
        return str(self.value_tok.value)
    
    def visit(self, ctx):
        res = RTResult()
        v = Boolean.before(self.value_tok.value)
        if v:
            return res.success(Boolean(v))
        return res.failure(AssignmentException(self.value_tok, 'Boolean', ctx))

class BinOpNode(Node):
    operations = {
        'PLUS': '__add__',
        'MINUS': '__sub__',
        'MUL': '__mul__',
        'DIV': '__div__',
        'POW': '__pow__',
        'NPOW': '__npow__',
        'EE': '__eq__',
        'LT': '__lt__',
        'GT': '__gt__',
        'LTE': '__lte__',
        'GTE': '__gte__',
        'NE': '__neq__'
    }

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
        op = self.operations.get(self.op_tok.type)
        if not op:
            return res.failure(OperationError(self.op_tok, type(left).__name__, 'Operator either does not exist or is invalid in this context', context))
        result = left.operation(op, right)
        if result[1]:
            return res.failure(OperationError(self.op_tok, type(left).__name__, result[1], context))
        return res.success(result[0])

class UnaryOpNode(Node):
    operations = {
        'PLUS': '__add__',
        'MINUS': '__sub__',
        'NOT': '__not__'
    }

    def __init__(self, op_tok, right_node):
        self.op_tok = op_tok
        self.right_node = right_node
        self.pos_start = op_tok.pos_start
        self.pos_end = right_node.pos_end

    def __repr__(self):
        return f'({self.op_tok.value} {self.right_node})'

    def visit(self, context):
        res = RTResult()
        right = res.register(self.right_node.visit(context))
        if res.error: return res
        op = self.operations.get(self.op_tok.type)
        if not op:
            return res.failure(OperationError(self.op_tok, type(right).__name__, 'Operator either does not exist or is invalid in this context', context))
        result = right.operation(op)
        if result[1]:
            return res.failure(OperationError(self.op_tok, type(right).__name__, result[1], context))
        return res.success(result[0])

class IfNode(Node):
    def __init__(self, comp, body, elseNodes):
        if not elseNodes: elseNodes = NodeList()
        self.elseNodes = elseNodes
        self.comp = comp
        self.body = body
        self.pos_start = comp.pos_start
        self.pos_end = body[len(body) - 1].pos_end
    
    def __repr__(self):
        return f'if ({self.comp}) {self.body}'

    def visit(self, context):
        res = RTResult()
        run = res.register(self.comp.visit(context))
        if res.error: return res
        result = run.operation('__truey__')
        if result[1]:
            return res.failure(OperationError(Token('?', '?', self.comp.pos_start, self.comp.pos_end), type(run).__name__, result[1], context))
        if result[0] == "true":
            data = res.register(iterateNodes(self.body, context))
            if res.error: return res
            return res.success(data)
        else:
            data = res.register(iterateNodes(self.elseNodes, context))
            if res.error: return res
            return res.success(data)
        return res.success(Undefined())

class ArrayNode(Node):
    def __init__(self, body=[]):
        self.body = body
        self.pos_start = 0
        self.pos_end = 0
        if len(body) > 0:
            self.pos_start = body[0].pos_start
            self.pos_end = body[0].pos_end
    
    def __repr__(self):
        return f'{body}'
    
    def visit(self, context):
        res = RTResult()
        value = Array()
        for v in self.body:
            val = res.register(v.visit(context))
            if res.error: return res
            value.operation('push', val)
        return res.success(value)

class VarCreateNode(Node):
    def __init__(self, name_tok, value_node):
        self.name_tok = name_tok
        self.value_node = value_node
        self.pos_start = name_tok.pos_start
        self.pos_end = value_node.pos_end
    
    def __repr__(self):
        return f'var {self.name_tok.value} = {self.value_node}'
    
    def visit(self, context):
        res = RTResult()
        value = res.register(self.value_node.visit(context))
        if res.error: return res
        if context.symbol_table.get(self.name_tok.value) != None:
            return res.failure(VarCreateException('Cannot re-declare variable\nRemove the `var` or `const` keyword to reassign', self.pos_start, self.pos_end, context))
        error = context.symbol_table.set(self.name_tok.value, value)
        if error != None:
            return res.failure(VarCreateException(error, self.pos_start, self.pos_end, context))
        return res.success(value)

class VarAssignNode(Node):
    def __init__(self, name_tok, value_node):
        self.name_tok = name_tok
        self.value_node = value_node
        self.pos_start = name_tok.pos_start
        self.pos_end = value_node.pos_end
    
    def __repr__(self):
        return f'{self.name_tok.value} = {self.value_node}'
    
    def visit(self, context):
        res = RTResult()
        value = res.register(self.value_node.visit(context))
        if res.error: return res
        if context.symbol_table.get(self.name_tok.value) == None:
            return res.failure(VarAssignmentException('Variable not declared', self.pos_start, self.pos_end, context))
        error = context.symbol_table.set(self.name_tok.value, value)
        if error != None:
            return res.failure(VarAssignmentException(error, self.pos_start, self.pos_end, context))
        return res.success(value)

class VarAccessNode(Node):
    def __init__(self, name_tok):
        self.name_tok = name_tok
        self.pos_start = name_tok.pos_start
        self.pos_end = name_tok.pos_end
    
    def __repr__(self):
        return str(self.name_tok.value)
    
    def visit(self, ctx):
        res = RTResult()
        value = ctx.symbol_table.get(self.name_tok.value)
        if value == None:
            return res.success(Undefined())
        return res.success(value)

class UndefNode(Node):
    def __init__(self, tok):
        self.pos_start = tok.pos_start
        self.pos_end = tok.pos_end
    
    def __repr__(self):
        return Undefined().__repr__()
    
    def visit(self, ctx):
        return RTResult().success(Undefined())

class FunctionNode(Node):
    def __init__(self, arg_toks, body_nodes, pos_start, pos_end, name_tok):
        self.arg_toks = arg_toks
        self.body_nodes = body_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.name_tok = name_tok

    def __repr__(self):
        return f'func ({self.arg_toks}) {self.body_nodes}'
    
    def visit(self, ctx):
        res = RTResult()
        if self.name_tok != None:
            name = self.name_tok.value
            value = Function(self.arg_toks, self.body_nodes, ctx, self.pos_start, self.pos_end, name)
            ctx.symbol_table.set(self.name_tok.value, value)
        else:
            name = '(anonymous)'
            value = Function(self.arg_toks, self.body_nodes, ctx, self.pos_start, self.pos_end, name)
        return res.success(value)

class CallNode(Node):
    def __init__(self, name_tok, arg_nodes, pos_end):
        self.pos_end = pos_end
        self.name = name_tok.value
        self.pos_start = name_tok.pos_start
        self.arg_nodes = arg_nodes
    
    def __repr__(self):
        return f'{self.name}({self.arg_nodes})'
    
    def visit(self, ctx):
        res = RTResult()
        function = ctx.symbol_table.get(self.name)
        if function == None:
            return res.failure(TypeException('Cannot call ' + Undefined().__repr__(), self.pos_start, self.pos_end, ctx))
        if not isinstance(function, FunctionValue):
            return res.failure(TypeException('Cannot call ' + type(function).__name__, self.pos_start, self.pos_end, ctx))
        if isinstance(function, BuiltinFunction):
            args = []
            for node in self.arg_nodes:
                val = res.register(node.visit(ctx))
                if res.error: return res
                args.append(val)
            value = function.execute(*args)
            if isinstance(value, RTResult):
                value = res.register(value)
                if res.error: return res
                return res.success(value)
            if value[1]:
                return res.failure(TypeException(value[1], sel.pos_start, self.pos_end, ctx))
            return res.success(value[0])
        value = res.register(function.execute(self.arg_nodes))
        if res.error: return res
        return res.success(value)

class ReturnNode(Node):
    def __init__(self, node, start, end):
        self.pos_start = start
        self.pos_end = end
        self.node = node
    
    def __repr__(self):
        return f'return {self.node};'
    
    def visit(self, ctx):
        res = RTResult(True)
        value = res.register(self.node.visit(ctx))
        if res.error: return res
        return res.success(value)

class StringNode(Node):
    def __init__(self, tok):
        self.pos_start = tok.pos_start
        self.pos_end = tok.pos_end
        self.text = tok.value[1:-1]
    
    def __repr__(self):
        return f"'{self.text}'"
    
    def visit(self, ctx):
        res = RTResult()
        val = String(self.text)
        return res.success(val)
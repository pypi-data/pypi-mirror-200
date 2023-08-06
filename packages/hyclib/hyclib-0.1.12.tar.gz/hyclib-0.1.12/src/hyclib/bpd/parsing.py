import re
import ast

allowed_nodes = (
    ast.Constant,
    ast.List,
    ast.Tuple,
    ast.Set,
    ast.Dict,
    ast.Name,
    ast.Load,
    ast.UnaryOp,
    ast.UAdd,
    ast.USub,
    ast.Not,
    ast.Invert,
    ast.BinOp,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.BitOr,
    ast.BitAnd,
    ast.BoolOp,
    ast.And,
    ast.Or,
    ast.Compare,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.Is,
    ast.IsNot,
    ast.In,
    ast.NotIn,
    ast.Subscript,
    ast.Slice,
)

def parse_var_names(expr):
    names = []
    for m in re.finditer('[^\\\](@)', expr):
        i = m.start(1)+1
        prev_s = None
        for j in range(1,len(expr) - i + 1):
            s = expr[i:i+j]
            if not s.isidentifier():
                if prev_s is None:
                    raise ValueError(f"No valid variable name found after @ at index {i}. {expr[i:]=}.")
                names.append(prev_s)
                break
            elif i + j == len(expr):
                names.append(s) # reached the end of string
            else:
                prev_s = s
    return names

def modify_expr(expr, names):
    def backtick_string_replacement(s):
        return f"BACKTICK_QUOTED_STRING_{s.group(0).replace(' ', '_').strip('`')}"

    expr = re.sub('`.*?`', backtick_string_replacement, expr)
    
    for name in names:
        expr = expr.replace(f'@{name}', f'__eval_local_{name}')
    
    parsed_expr = ast.parse(expr)
    if len(parsed_expr.body) != 1:
        raise ValueError(f"expr must consist of a single expression, but {len(parsed_expr.body)=}.")
        
    stmt = parsed_expr.body[0]
    if not isinstance(stmt, ast.Expr):
        raise ValueError(f"expr must be an expression, but {type(stmt)=}.")
    
    class Transformer(ast.NodeTransformer):
        def visit_BoolOp(self, node):
            values = [Transformer().visit(value) for value in node.values] # transform child nodes first
            
            if isinstance(node.op, ast.And):
                op = ast.BitAnd()
            elif isinstance(node.op, ast.Or):
                op = ast.BitOr()
            else:
                raise RuntimeError(f"node.op should be ast.And or ast.Or, but got {node.op=}.")
            
            if len(values) < 2:
                raise RuntimeError(f"Length of node.values should be at least 2, but got {len(values)=}.")
                
            bin_op = ast.BinOp(values.pop(0), op, values.pop(0))
            while len(values) > 0:
                bin_op = ast.BinOp(bin_op, op, values.pop(0))
                
            return bin_op
        
        def visit_UnaryOp(self, node):
            operand = Transformer().visit(node.operand)
            
            op = ast.Invert() if isinstance(node.op, ast.Not) else node.op
            return ast.UnaryOp(op, operand)

    parsed_expr.body[0].value = Transformer().visit(stmt.value)
    
    for node in ast.walk(parsed_expr.body[0].value):
        if not isinstance(node, allowed_nodes):
            raise ValueError(f"{node=} is not allowed in expression.") # Some basic effort to prevent arbitrary code execution.
            
    return ast.unparse(parsed_expr)
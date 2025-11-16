import sys
import ast
import operator

env = {}

allowed_ops = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
}

def safe_eval(node):
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.Name):
        if node.id in env:
            return env[node.id]
        raise NameError(f"{node.id} は未定義です")
    elif isinstance(node, ast.BinOp) and type(node.op) in allowed_ops:
        return allowed_ops[type(node.op)](safe_eval(node.left), safe_eval(node.right))
    else:
        raise ValueError("Unsupported operation")

def eval_expr(expr):
    expr = expr.strip()
    if "->" in expr and "|" in expr:
        cond, rest = expr.split("->")
        true_val, false_val = rest.split("|")
        cond_val = eval_expr(cond)
        return eval_expr(true_val) if cond_val else eval_expr(false_val)
    
    if "->" in expr and "|" not in expr:
        start, end = expr.split("->")
        start, end = int(eval_expr(start)), int(eval_expr(end))
        return list(range(start, end + 1))
    
    tree = ast.parse(expr, mode="eval").body
    return safe_eval(tree)

def run_line(line):
    line = line.strip()
    if not line:
        return
    
    if line.startswith("print "):
        val = eval_expr(line[len("print "):])
        if isinstance(val, list):
            for v in val:
                print(v)
        else:
            print(val)
        return
    
    if "=" in line:
        var, expr = line.split("=", 1)
        var, val = var.strip(), eval_expr(expr)
        env[var] = val
        return

def run_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            run_line(line)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python Cequal2.py program.c2")
    else:
        run_file(sys.argv[1])

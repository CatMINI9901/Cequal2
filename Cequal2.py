import sys

env = {}

def eval_expr(expr):
    if "->" in expr and "|" in expr:
        cond, rest = expr.split("->")
        true_val, false_val = rest.split("|")
        cond = eval(cond, {}, env)
        return eval(true_val if cond else false_val, {}, env)

    if "->" in expr and "|" not in expr:
        start, end = expr.split("->")
        start, end = int(eval(start, {}, env)), int(eval(end, {}, env))
        return list(range(start, end+1))

    return eval(expr, {}, env)

def run_line(line):
    line = line.strip()
    if not line: return

    if line == "C=2":
        env["C"] = 2
        print("Cは2に決定された")
        return

    if line.startswith("print "):
        expr = line[len("print "):]
        val = eval_expr(expr)
        if isinstance(val, list):
            for v in val: print(v)
        else:
            print(val)
        return

    if "=" in line:
        var, expr = line.split("=", 1)
        var = var.strip()
        val = eval_expr(expr)
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

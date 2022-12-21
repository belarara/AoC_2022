from collections import deque
from sympy import Symbol, Eq, solve
with open("21/input", "r") as f:
    data = f.read()

operations = {
    "*": lambda x,y: x*y,
    "+": lambda x,y: x+y,
    "-": lambda x,y: x-y,
    "/": lambda x,y: x//y,
    "=": lambda x,y: (x,y)
}

monkeys = {}
for line in [a for a in data.split("\n") if a!=""]:
    spl = line.split(" ")
    monkey = spl[0][:-1]
    if len(spl)==2:
        monkeys[monkey] = int(spl[1])
    else:
        monkeys[monkey] = (spl[2], spl[1], spl[3])

def create_solves(monkeys):
    solved = {k:v for k,v in monkeys.items() if type(v) is int}
    partial_solved = {}
    for k,v in monkeys.items():
        if type(v)==tuple:
            p,q = v[1],v[2]
            if p not in partial_solved: partial_solved[p]=set()
            if q not in partial_solved: partial_solved[q]=set()
            if p in solved:
                partial_solved[q].add(k)
            elif q in solved:
                partial_solved[p].add(k)
            else:
                partial_solved[p].add(k)
                partial_solved[q].add(k)
    return solved, partial_solved

def solve_partial(monkeys, solved, partial_solved):
    queue = list(solved.keys())
    while len(queue)>0:
        solve = queue.pop()
        if solve in partial_solved:
            for v in partial_solved[solve].copy():
                operand, dep1, dep2 = monkeys[v]
                if dep1 in solved and dep2 in solved:
                    solved[v] = operations[operand](solved[dep1], solved[dep2])
                    queue.append(v)
                    partial_solved[solve] -= {v}
    return solved, partial_solved

s,p = create_solves(monkeys)
s,p = solve_partial(monkeys, s, p)
print(f"1) {s['root']}")

monkeys_v2 = monkeys.copy()
monkeys_v2["root"] = ("=", monkeys_v2["root"][1], monkeys_v2["root"][2])
del monkeys_v2["humn"]
solved, partial_solved = create_solves(monkeys_v2)
removed_partial = partial_solved.pop("humn")
solved_v2,partial_v2 = solve_partial(monkeys_v2, solved, partial_solved)
partial_v2["humn"] = removed_partial

def create_eq(var, operation, op1, op2):
    if operation == "+": return Eq((op1+op2), var)
    if operation == "-": return Eq((op1-op2), var)
    if operation == "*": return Eq((op1*op2), var)
    if operation == "/": return Eq((op1/op2), var)
    if operation == "=": return Eq(op1, op2)

monkeys_v2["humn"] = 0
unsolved = {k:v for k,v in monkeys_v2.items() if k not in solved_v2}
symbols = {k:Symbol(k) for k in unsolved}
eqs = []
for k in unsolved:
    if k != "humn":
        operation, dep1, dep2 = monkeys_v2[k]
        if dep1 in solved_v2: sb1 = solved_v2[dep1]
        else:                 sb1 = symbols[dep1]
        if dep2 in solved_v2: sb2 = solved_v2[dep2]
        else:                 sb2 = symbols[dep2]
        eqs.append(create_eq(symbols[k], operation, sb1, sb2))

sol = solve(eqs, list(symbols.values()))
print(f"2) {sol[symbols['humn']]}")
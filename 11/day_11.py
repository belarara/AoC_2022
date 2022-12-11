with open("11/input", "r") as f:
    data = f.read()

def make_lambda(sign, val):
    if val.isdigit():
        val = int(val)
        if sign == "*":
            return lambda old: old*val
        elif sign == "+":
            return lambda old: old+val
    else:
        if sign == "*":
            return lambda old: old*old
        elif sign == "+":
            return lambda old: old+old
    return lambda old: "_"

def get_monkeys(data):
    dsp = data.split("\n")
    monkeys = {}
    for monkey in range(0,len(dsp)//7):
        monkeys[monkey] = {}
        monkeys[monkey]["Starting items"] = [int(a[:-1]) if a.endswith(",") else int(a) for a in dsp[monkey*7+1].split(" ")[4:]]
        monkeys[monkey]["Test"] = int(dsp[monkey*7+3].split(" ")[-1])
        monkeys[monkey][True] = int(dsp[monkey*7+4].split(" ")[-1])
        monkeys[monkey][False] = int(dsp[monkey*7+5].split(" ")[-1])
        spl = dsp[monkey*7+2].split(" ")
        monkeys[monkey]["Operation"] = make_lambda(spl[-2], spl[-1])
    return monkeys

m = get_monkeys(data)
rounds = 20
inspections = [0]*len(m)
for i in range(rounds):
    for k,v in m.items():
        for j in range(len(v["Starting items"])):
            e = v["Starting items"].pop(0)
            new = v["Operation"](e)//3
            m[v[new%v["Test"]==0]]["Starting items"].append(new)
            inspections[k]+=1

x = sorted(inspections, reverse=True)
print(f"1) {x[0]*x[1]}")

monkeys = get_monkeys(data)
rounds = 10000
modulo = 1
for v in monkeys.values():
    modulo *= v["Test"]
inspections = [0]*len(monkeys)
for i in range(rounds):
    for k,v in monkeys.items():
        for j in range(len(v["Starting items"])):
            e = v["Starting items"].pop(0)
            new = v["Operation"](e)%modulo
            monkeys[v[new%v["Test"]==0]]["Starting items"].append(new)
            inspections[k]+=1

x = sorted(inspections, reverse=True)
print(f"2) {x[0]*x[1]}")
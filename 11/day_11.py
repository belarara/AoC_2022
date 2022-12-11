import copy
monkeys = {
    0: {
        "Starting items": [54,89,94],
        "Operation": lambda old: old*7,
        "Test": 17,
        True: 5,
        False: 3
    },
    1: {
        "Starting items": [66,71],
        "Operation": lambda old: old+4,
        "Test": 3,
        True: 0,
        False: 3
    },
    2: {
        "Starting items": [76, 55, 80, 55, 55, 96, 78],
        "Operation": lambda old: old+2,
        "Test": 5,
        True: 7,
        False: 4
    },
    3: {
        "Starting items": [93, 69, 76, 66, 89, 54, 59, 94],
        "Operation": lambda old: old+7,
        "Test": 7,
        True: 5,
        False: 2
    },
    4: {
        "Starting items": [80, 54, 58, 75, 99],
        "Operation": lambda old: old*17,
        "Test": 11,
        True: 1,
        False: 6
    },
    5: {
        "Starting items": [69, 70, 85, 83],
        "Operation": lambda old: old+8,
        "Test": 19,
        True: 2,
        False: 7
    },
    6: {
        "Starting items": [89],
        "Operation": lambda old: old+6,
        "Test": 2,
        True: 0,
        False: 1
    },
    7: {
        "Starting items": [62, 80, 58, 57, 93, 56],
        "Operation": lambda old: old*old,
        "Test": 13,
        True: 6,
        False: 4
    }
}

m = copy.deepcopy(monkeys)
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
import ast

with open("13/input") as f:
    data = f.read().split("\n")

def parse_line(line):
    return ast.literal_eval(line)

def compare(a,b):
    if type(a) is int:
        if type(b) is int:
            if a>b: return -1
            if a<b: return 1
            if a==b: return 0
        return compare([a],b)
    if type(b) is int:
        return compare(a, [b])
    for i,j in list(zip(a,b[:len(a)])):
        c = compare(i,j)
        if c==1: return 1
        if c==-1: return -1
    if len(a)>len(b): return -1
    elif len(a)<len(b): return 1
    else: return 0

s = [compare(parse_line(data[i]), parse_line(data[i+1])) for i in range(0,len(data),3)]
print(f"{sum([i+1 for i,e in enumerate([a==1 for a in s]) if e])}")

data_all = [parse_line(a) for a in data if a.startswith("[")]+[[[2]], [[6]]]
for i in range(len(data_all)):
    for j in range(i+1, len(data_all)):
        if compare(data_all[i], data_all[j])>0:
            x = data_all[i]
            data_all[i] = data_all[j]
            data_all[j] = x
p = 1
for i,e in enumerate(reversed(data_all)):
    if e in [[[2]], [[6]]]: p*=i+1
print(f"2) {p}")
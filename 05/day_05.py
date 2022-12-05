import re, copy

with open("05/input", "r") as f:
    data = f.read()
stacks = {}
moves = []
for i in data.split("\n"):
    if i != "":
        if i.startswith("move"):
            a,b,c = re.search(r"(\b\d+\b).*(\b\d+\b).*(\b\d+\b)", i).groups()
            moves.append([int(x) for x in (a,b,c)])
        else:
            for j,e in enumerate(range(1,len(i),4)):
                if j not in stacks.keys():
                    stacks[j] = []
                if i[e] != " ":
                    stacks[j].insert(0, i[e])

def do_moves(stack_dict, move_list, rev=True):
    st = copy.deepcopy(stack_dict)
    for a,b,c in move_list:
        tm = st[b-1][-a:]
        st[b-1]=st[b-1][:-a]
        if rev:
            tm = list(reversed(tm))
        st[c-1] += tm
    s = []
    for k,v in st.items():
        s += v[-1]
    return s

print(f"1) {''.join(do_moves(stacks, moves, True))}")
print(f"2) {''.join(do_moves(stacks, moves, False))}")
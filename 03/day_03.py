f = open("03/input", "r")
data = f.read().split("\n")
data = [a for a in data if a!=""]

def char_to_priority(c):
    p = ord(c)
    if p>=65 and p<=90:
        return p-38
    elif p>=97 and p<=122:
        return p-96
    else:
        raise ValueError

rucksacks_duplicates = {}
for i,r in enumerate(data):
    h = len(r)//2
    p,q = r[:h], r[h:]
    p_prio = [char_to_priority(a) for a in p]
    q_prio = [char_to_priority(a) for a in q]
    rucksacks_duplicates[i] = []
    for a in p_prio:
        if a in q_prio and a not in rucksacks_duplicates[i]:
            rucksacks_duplicates[i].append(a)

print(f"1) {sum([sum(a) for a in rucksacks_duplicates.values()])}")

def find_badge(ls):
    a,b,c = ls
    badge_a_bc = [o for o in a if o in b and o in c]
    badge_b_c  = [o for o in b if o in c]
    return list(set([o for o in badge_a_bc if o in badge_b_c]))

groups = [data[i:i+3] for i in range(0, len(data), 3)]
badges = [find_badge(o) for o in groups if len(o)==3]
badges_prio = [sum([char_to_priority(a) for a in b]) for b in badges]
print(f"2) {sum(badges_prio)}")
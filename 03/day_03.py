f = open("03/input", "r")
data = f.read().split("\n")
data = [a for a in data if a!=""]

def char_to_priority(c):
    p = ord(c)
    if p>=65 and p<=90: return p-38
    elif p>=97 and p<=122: return p-96

count = 0
data_prio = [[char_to_priority(a) for a in b] for b in data]
for line in data_prio:
    a,b = set(line[:len(line)//2]), set(line[len(line)//2:])
    count += sum(a.intersection(b))
print(f"1) {count}")

groups = [data_prio[i:i+3] for i in range(0, len(data_prio), 3)]
badges = [sum(set(a).intersection(set(b).intersection(set(c)))) for a,b,c in groups]
print(f"2) {sum(badges)}")
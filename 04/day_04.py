f = open("04/input", "r")
data = [a for a in f.read().split("\n") if a != ""]
pairs = [a.split(",") for a in data]
pairs_split = [([int(a) for a in p.split("-")], [int(a) for a in q.split("-")]) for p,q in pairs]

count = 0
for ((a,b),(c,d)) in pairs_split:
    if (a<=c and b>=d) or (c<=a and d>=b):
        count += 1
print(f"1) {count}")

overlaps = 0
for ((a,b),(c,d)) in pairs_split:
    if a<=d and b>=c:
        overlaps += 1
print(f"2) {overlaps}")
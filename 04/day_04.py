f = open("04/input", "r")
data = [a for a in f.read().split("\n") if a != ""]
pairs = [a.split(",") for a in data]
pairs_split = [([int(a) for a in p.split("-")], [int(a) for a in q.split("-")]) for p,q in pairs]
print(f"1) {sum([1 for ((a,b),(c,d)) in pairs_split if (a<=c and b>=d) or (c<=a and d>=b)])}")
print(f"2) {sum([1 for ((a,b),(c,d)) in pairs_split if a<=d and b>=c])}")
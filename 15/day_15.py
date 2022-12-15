import re
fn = "15/input"
with open(fn) as f:
    data = f.read().split("\n")

groups = [[list(map(int, b)) for b in re.findall("x=(-?\d+), y=(-?\d+)", a)] for a in data if a != ""]

def manh_distance(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

def overlap(a,b):
    if a[0] in range(b[0],b[1]+1) or a[1] in range(b[0],b[1]+1):
        return True
    return False

y = 2000000
ls = []
for sensor,beacon in groups:
    md = manh_distance(sensor, beacon)
    a = abs(sensor[1]-y)
    if a<=md:
        ls.append((sensor[0]-(md-a),sensor[0]+(md-a)))

xs = []
while len(ls)>0:
    ol = True
    x = ls.pop()
    while ol:
        ol = False
        for i in ls:
            if overlap(x,i) or overlap(i,x):
                x = (min(x[0],i[0]), max(x[1],i[1]))
                ls.remove(i)
                ol = True
    xs.append(x)
print(f"1) {sum([abs(a-b) for a,b in xs])}")

bd = [(0,20+1),(0,20+1)] if fn.endswith("test") else [(0,4000000+1), (0, 4000000+1)]
g_dist = [[s, manh_distance(s,b)] for s,b in groups]

done, pt = False, None
for (s1,s2), dist in g_dist: # iterate over sensors
    for i in range(dist+2): # generate all points on border outside the manh distance from sensor,beacon
        add = [a for a in
            [(s1-i, s2-(dist+1-i)),
            (s1-i, s2+(dist+1-i)),
            (s1+i, s2-(dist+1-i)),
            (s1+i, s2+(dist+1-i)),]
            if a[0] in range(*bd[0]) and a[1] in range(*bd[1])
        ]
        add
        for a in add:
            _break = True
            for s,d in g_dist: # for each point check if within manh distance from sensor
                if manh_distance(s,a)<=d:
                    _break = False
                    break
            if _break:
                pt = a
                done = True
                break
        if done: break
    if done: break

i,j = pt
print(f"2) {pt[0]*4000000+pt[1]}")
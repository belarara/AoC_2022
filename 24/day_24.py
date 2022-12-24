import heapq, time
with open("24/input", "r") as f:
    data = f.read()

direction_from_string = {"^":0,">":1,"v":2,"<":3}
direction_to_string = ["^",">","v","<"]
direction = [(-1, 0), (0, 1), (1, 0),(0, -1)]

def point_add(p1,p2,mx,my):
    x,y = p1[0]+p2[0], p1[1]+p2[1]
    if x<1: x=mx-2
    elif x>mx-2: x=1
    if y<1: y=my-2
    elif y>my-2: y=1
    return x,y

def animate_blizzard(blizzard, mx, my):
    new = {}
    for k,v in blizzard.items():
        for d in v:
            new_p = point_add(k, direction[d], mx, my)
            if new_p not in new: new[new_p] = []
            new[new_p].append(d)
    return new

def prt(bliz, pos, mx, my):
    ls = [["#" for y in range(my)] for x in range(mx)]
    for i in range(len(ls)):
        for j in range(len(ls[0])):
            if (i,j) in bliz:
                ls[i][j] = direction_to_string[bliz[(i,j)][0]]
                if len(bliz[(i,j)])>1:
                    ls[i][j] = str(len(bliz[(i,j)]))
            elif i>0 and i<max_x-1 and j>0 and j<max_y-1:
                ls[i][j] = "."
    ls[0][1], ls[-1][-2] = ".", "."
    if ls[pos[0]][pos[1]]==".":
        ls[pos[0]][pos[1]] = "E"
    else:
        ls[pos[0]][pos[1]] = "x"
    return "\n".join(["".join(a) for a in ls])


def next_possible(next_bliz, pos, mx, my):
    allowed = [pos]+[(pos[0]+x, pos[1]+y) for x,y in direction]
    possible = []
    for px,py in allowed:
        if (px>0 and py>0 and px<mx-1 and py<my-1 and (px,py) not in next_bliz) or ((px,py) in [(0,1),(mx-1,my-2)]):
            possible.append((px,py))
    return possible

def distance(pos1,pos2):
    return abs((pos2[0]-pos1[0]))+abs((pos2[1]-pos1[1]))

t0 = time.time()
spl = [a for a in data.split("\n") if a!=""]
max_x,max_y = len(spl), len(spl[0])
blizzards = {}
for i in range(len(spl)):
    for j in range(len(spl[0])):
        if spl[i][j] in "^>v<":
            blizzards[(i,j)] = [direction_from_string[spl[i][j]]]

repeat = max_x*max_y
blizzard_round = [blizzards]
for i in range(repeat):
    blizzard_round.append(animate_blizzard(blizzard_round[-1], max_x, max_y))
    if blizzard_round[-1]==blizzard_round[0] and i<repeat:
        repeat = i+1


def walk_fastest(states, blizzard_rounds, mx, my, end):
    repeat = len(blizzard_round)
    visited = set()
    heapq.heapify(states)
    while len(states)>0:
        _, ((curr_x, curr_y), minute) = heapq.heappop(states)
        if (curr_x, curr_y) == end:
            return minute
        if ((curr_x, curr_y), minute%repeat) in visited:
            continue
        visited.add(((curr_x, curr_y), minute%repeat))
        next_pos = next_possible(blizzard_rounds[(minute+1)%repeat], (curr_x, curr_y), mx, my)
        for x,y in next_pos:
            if ((x,y), (minute+1)%repeat) not in visited:
                heapq.heappush(states, (minute+1+distance((x,y), end), ((x,y), minute+1)))
t1 = time.time()
start,end = (0,1),(max_x-1,max_y-2)
time1 = walk_fastest([(distance(start,end), (start, 0))], blizzard_round, max_x, max_y, end) # distance, (position, minute)
print(f"1) {time1}")
t2 = time.time()

time2 = walk_fastest([(distance(end, start), (end, time1))], blizzard_round, max_x, max_y, start)
time3 = walk_fastest([(distance(start, end), (start, time2))], blizzard_round, max_x, max_y, end)
print(f"2) {time3}")
t3 = time.time()
print(f"Times:")
print(f"generate blizzards) {t1-t0}")
print(f"1) {t2-t1}")
print(f"2) {t3-t2}")
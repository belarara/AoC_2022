import time
with open("23/input", "r") as f:
    data = f.read()

field = [[b=="#" for b in a] for a in data.split("\n") if a != ""]

def expand(field):
    x,y = len(field), len(field[0])
    new = [[False]*(y+2)]
    for i in range(x):
        new.append([False] + field[i] + [False])
    return new + [[False]*(y+2)]

def reduce(field):
    x_min, x_max, y_min, y_max = len(field)-1, 0, len(field[0])-1, 0
    for i in range(len(field)):
        for j in range(len(field[i])):
            if i<x_min and field[i][j]: x_min = i
            if i>x_max and field[i][j]: x_max = i
            if j<y_min and field[i][j]: y_min = j
            if j>y_max and field[i][j]: y_max = j
    return [[field[i][j] for j in range(y_min,y_max+1)] for i in range(x_min, x_max+1)]

def print_field(field):
    for r in field:
        print("".join(["#" if a else "." for a in r]))

surround = [(-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1)]
directions = [[(-1,-1),(-1,0),(-1,1)],[(1,-1),(1,0),(1,1)],[(-1,-1),(0,-1),(1,-1)],[(-1,1),(0,1),(1,1)]]

def get_point(field, point, point_add=(0,0)):
    x,y = (point[0]+point_add[0], point[1]+point_add[1])
    if x>=0 and x<len(field) and y>=0 and y<len(field[x]):
        return field[x][y]
    return False

def propose(field, step):
    proposals = {}
    for i in range(len(field)):
        for j in range(len(field[0])):
            if field[i][j] and any([get_point(field, (i,j), surr_p) for surr_p in surround]):
                for dir_points in [directions[(step+m)%4] for m in range(4)]:
                    if all([not get_point(field, (i,j), point) for point in dir_points]):
                        new_pos = (i+dir_points[1][0], j+dir_points[1][1])
                        if new_pos not in proposals: proposals[new_pos] = (i,j)
                        else: del proposals[new_pos]
                        break
    return proposals

t1=time.time()
field_v1 = reduce(field)
for i in range(10):
    field_v1 = expand(field_v1)
    props = propose(field_v1, i)
    for (x,y),(p,q) in props.items():
        field_v1[x][y], field_v1[p][q] = True, False
print(f"1) {sum([sum([not a for a in row]) for row in reduce(field_v1)])}")
t2=time.time()

field_v2 = field
count = 0
props = {1:1}
while len(props)>0:
    if count%10==0: field_v2 = reduce(field_v2)
    field_v2 = expand(field_v2)
    props = propose(field_v2, count)
    for (x,y),(p,q) in props.items():
        field_v2[x][y], field_v2[p][q] = True, False
    count += 1
print(f"2) {count}")
t3=time.time()

def point_add(p1,p2):
    return (p1[0]+p2[0], p1[1]+p2[1])

def move_elves(elves, round):
    new_positions = {}
    for elf in elves:
        if all([(point_add(elf, surr) not in elves) for surr in surround]):
            new_positions[elf] = elf
        else:
            moved = False
            for dirs in [directions[(round+m)%4] for m in range(4)]:
                if all([(point_add(elf, d) not in elves) for d in dirs]):
                    moved = True
                    np = point_add(elf,dirs[1])
                    if np not in new_positions: new_positions[np] = elf
                    else:
                        new_positions[new_positions[np]] = new_positions[np]
                        del new_positions[np]
                        new_positions[elf] = elf
                    break
            if not moved:
                new_positions[elf] = elf
    ret = set(new_positions.keys())
    return ret, elves!=ret

def get_empty_squares(elves):
    _x,x_ = min(elves, key=lambda o:o[0])[0],max(elves, key=lambda o:o[0])[0]
    _y,y_ = min(elves, key=lambda o:o[1])[1],max(elves, key=lambda o:o[1])[1]
    return (x_-_x+1)*(y_-_y+1)-len(elves)

t4=time.time()
elves = set()
for i in range(len(field)):
    for j in range(len(field[0])):
        if field[i][j]:
            elves.add((i,j))

for i in range(10):
    elves, _ = move_elves(elves, i)
print(f"1) {get_empty_squares(elves)}")
t5=time.time()

changed = True
while changed:
    i+=1
    elves, changed = move_elves(elves, i)
print(f"2) {i+1}")
t6=time.time()

print("times")
print(f"1 grid) {t2-t1}")
print(f"2 grid) {t3-t2}")
print(f"1 set)  {t5-t4}")
print(f"2 set)  {t6-t5}")
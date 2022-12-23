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
                    ls = [not get_point(field, (i,j), point) for point in dir_points]
                    if all(ls):
                        new_pos = (i+dir_points[1][0], j+dir_points[1][1])
                        if new_pos not in proposals: proposals[new_pos] = (i,j)
                        else: del proposals[new_pos]
                        break
    return proposals

field_v1 = reduce(field)
for i in range(10):
    field_v1 = expand(field_v1)
    props = propose(field_v1, i)
    for (x,y),(p,q) in props.items():
        field_v1[x][y], field_v1[p][q] = True, False
print(f"1) {sum([sum([not a for a in row]) for row in reduce(field_v1)])}")

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
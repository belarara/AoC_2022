with open("22/input", "r") as f:
    data = f.read()

lines = [a for a in data.split("\n") if a != ""]
path = lines[-1]
maze_row_len = max([len(line) for line in lines[:-1]])
maze_col_len = len(lines[:-1])
maze = [line+(maze_row_len-len(line))*" " for line in lines[:-1]]

direction = {
    0: (-1, 0), # up
    1: (0,  1), # right
    2: (1,  0), # down
    3: (0, -1), # left
}

# calculate the next field for each direction
next = {}
for i in range(maze_col_len):
    for j in range(maze_row_len):
        if maze[i][j] == ".":
            for k, (p,q) in direction.items():
                x,y = (i+p)%maze_col_len, (j+q)%maze_row_len
                while maze[x][y] == " ":
                    x,y = (x+p)%maze_col_len, (y+q)%maze_row_len
                next[(i,j,k)] = (x,y) if maze[x][y] == "." else (i,j)

# create a list from path input with either direction change or steps to move
i = 0
path_list = []
while i<len(path):
    j = 1
    while i+j<len(path):
        if path[i+j] in "LR":
            break
        j += 1
    path_list.append(int(path[i:i+j]))
    if i+j<len(path):
        path_list.append(path[i+j])
    i += j+1

# follow the path by looking up the next field
cur_dir, cur_pos = 1, (0,maze[0].find("."))
for o in path_list:
    if o in ["L", "R"]:
        cur_dir = (cur_dir + (1 if o=="R" else -1))%4
    else:
        for c in range(o):
            next_pos = next[(cur_pos[0], cur_pos[1], cur_dir)]
            if next_pos == cur_pos: break
            cur_pos = next_pos

print(f"1) {(cur_pos[0]+1)*1000+(cur_pos[1]+1)*4+((cur_dir-1)%4)}")

# calculate how many neighbors on the map are not on a cube face
def blank_neighbors(maze, x,y):
    c,r = len(maze), len(maze[0])
    neighbors = []
    for a,b in [(x+p,y+q) for p,q in direction.values()]:
        if a<0 or a>=c or b<0 or b>=r or maze[a][b]==" ":
            neighbors.append((a,b))
    return neighbors

# calculate length of a cube face
sides = []
for i in range(maze_col_len):
    sides.append(len([1 for j in range(maze_row_len) if maze[i][j] in ".#"]))
for j in range(maze_row_len):
    sides.append(len([1 for i in range(maze_col_len) if maze[i][j] in ".#"]))
side_len = min(sides)

# for each outward facing edge create list of fields, and facing direction for edge fields
cube_wrap = {}
facing, moving = 0, 1
start = (0, maze[0].find("."))
x,y = start
for side in range(14):
    cube_wrap[side] = {}
    move_x, move_y = direction[moving]
    face_x, face_y = direction[facing]
    cube_wrap[side]["LIST"] = []
    cube_wrap[side]["facing"] = facing
    cube_wrap[side]["start"] = len(blank_neighbors(maze, x-move_x,y-move_y))
    for k in range(side_len):
        cube_wrap[side]["LIST"].append(((x,y),(x+face_x, y+face_y)))
        x,y = x+move_x, y+move_y
    cube_wrap[side]["end"] = len(blank_neighbors(maze, x, y))
    if cube_wrap[side]["end"] == 3:
        facing,moving = (facing+1)%4, (moving+1)%4
        x,y = x-move_x, y-move_y
    elif cube_wrap[side]["end"] == 0:
        facing,moving = (facing-1)%4, (moving-1)%4
        x,y = x+face_x, y+face_y

# calculate the next field for each field and direction, that is not an outwards facing field
next_cube = {}
for i in range(maze_col_len):
    for j in range(maze_row_len):
        if maze[i][j] == ".":
            for k, (p,q) in direction.items():
                x,y = (i+p), (j+q)
                if x>=0 and x<maze_col_len and y>=0 and y<maze_row_len:
                    if   maze[x][y] == ".": next_cube[(i,j,k)] = (x,y,k)
                    elif maze[x][y] == "#": next_cube[(i,j,k)] = (i,j,k)

def wrap_lookup(a,b):
    if a+b>3: return {(3,3): 1, (3,1): 0, (1,3): 0}[(a,b)]
    return -1

# create next fields for each edge that connects on the cube
for i in range(7):
    for side in range(14):
        if cube_wrap[side]["start"] == 0:
            for j in range(1,14):
                if cube_wrap[(side-j)%14]["end"]==0:
                    before = (side-j)%14
                    break
            new_after, new_before = side, before
            for j in range(12):
                if cube_wrap[(side+j)%14]["start"] > 0 and new_after==side: new_after  = (side+j)%14
                if cube_wrap[(before-j)%14]["end"] > 0 and new_before==before: new_before = (before-j)%14
            after_list, before_list = cube_wrap[side]["LIST"], list(reversed(cube_wrap[before]["LIST"]))
            for c in range(len(after_list)):
                ((p1,p2), (_,_)), ((q1,q2), (_,_)) = after_list[c], before_list[c]
                if maze[q1][q2] == ".":
                    next_cube[(p1,p2,cube_wrap[side]["facing"])] = (q1,q2,(cube_wrap[before]["facing"]+2)%4)
                else:
                    next_cube[(p1,p2,cube_wrap[side]["facing"])] = (p1,p2,cube_wrap[side]["facing"])
                if maze[p1][p2] == ".":
                    next_cube[(q1,q2,cube_wrap[before]["facing"])] = (p1,p2,(cube_wrap[side]["facing"]+2)%4)
                else:
                    next_cube[(q1,q2,cube_wrap[before]["facing"])] = (q1,q2,cube_wrap[before]["facing"])
            cube_wrap[side]["start"], cube_wrap[side]["end"] = -1, -1
            cube_wrap[before]["start"], cube_wrap[before]["end"] = -1, -1
            wrap_look = wrap_lookup(cube_wrap[new_before]["end"], cube_wrap[new_after]["start"])
            cube_wrap[new_before]["end"], cube_wrap[new_after]["start"] = wrap_look, wrap_look
            break

# follow the path with cube field lookup
cur_dir, cur_pos = 1, (0,maze[0].find("."))
took = []
for o in path_list:
    if o in ["L", "R"]:
        cur_dir = (cur_dir + (1 if o=="R" else -1))%4
    else:
        for c in range(o):
            took.append((cur_pos[0], cur_pos[1], cur_dir))
            next_x, next_y, face = next_cube[(cur_pos[0], cur_pos[1], cur_dir)]
            if (next_x, next_y) == cur_pos: break
            cur_pos = next_x, next_y
            cur_dir = face

print(f"2) {(cur_pos[0]+1)*1000+(cur_pos[1]+1)*4+((cur_dir-1)%4)}")

# draw the maze (uncomment the 'took' list above)
def draw_maze(maze, path_taken):
    dirs = {0:"^",1:">",2:"v",3:"<"}
    nm = [list(a) for a in maze]
    for p1,p2,d in path_taken:
        nm[p1][p2] = dirs[d]
    s = ""
    for i in range(4):
        col = [str(int((a//(1*(10**i)))%10)) for a in range(maze_row_len)]
        for x in range(len(col)):
            if col[x]!="0":
                break
            col[x] = " "
        s += "      " + ''.join(col) + "\n"
    for i,l in enumerate(nm):
        s += f"{(4-len(str(i)))*' '}{i}  {''.join(l)}\n"
    return s

with open("22/maze.txt", "w") as f:
    f.write(draw_maze(maze, took))
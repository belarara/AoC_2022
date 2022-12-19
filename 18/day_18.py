from collections import deque
with open("18/input", "r") as f:
    data = f.read().split("\n")

coords = [tuple(int(a) for a in b.split(",")) for b in data if b != ""]

def create_coord_dict(coords):
    blocks = {0:{},1:{},2:{}}
    for i in range(3):
        for coord in coords:
            if (coord[i%3], coord[(i+1)%3]) not in blocks[i]:
                blocks[i][(coord[i%3], coord[(i+1)%3])] = set()
            blocks[i][(coord[i%3], coord[(i+1)%3])].add(coord[(i+2)%3])
    return blocks

def count_edges_in_blocks(blocks):
    count_edges = 0
    for i in range(3):
        for key in blocks[i].keys():
            found = False
            max_value = max(blocks[i][key])
            for j in range(max_value+4):
                if not found and j in blocks[i][key]:
                    found = True
                    count_edges += 2
                elif found and j not in blocks[i][key]:
                    found = False
    return count_edges


print(f"1) {count_edges_in_blocks(create_coord_dict(coords))}")

max_x, max_y, max_z = max([a[0] for a in coords]), max([a[1] for a in coords]), max([a[2] for a in coords])

extended_coords = list(coords)
for xx in range(1,max_x):
    for yy in range(1,max_y):
        for zz in range(1,max_z):
            if (xx,yy,zz) not in extended_coords:
                touch_border = False
                add_pocket = []
                queue = deque([(xx,yy,zz)])
                while len(queue)>0 and not touch_border:
                    x,y,z = queue.pop()
                    neighbors = [(x-1,y,z),(x+1,y,z), (x,y-1,z),(x,y+1,z), (x,y,z-1),(x,y,z+1)]
                    for n in neighbors:
                        if (n not in queue
                        and n not in add_pocket
                        and n not in extended_coords):
                            if n[0]>0 and n[0]<max_x and n[1]>0 and n[1]<max_y and n[2]>0 and n[2]<max_z:
                                queue.append(n)
                            else:
                                touch_border = True
                    add_pocket.append((x,y,z))
                if not touch_border:
                    extended_coords += add_pocket

print(f"2) {count_edges_in_blocks(create_coord_dict(extended_coords))}")
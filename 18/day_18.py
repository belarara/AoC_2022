with open("18/input", "r") as f:
    data = f.read().split("\n")

coords = [tuple(int(a) for a in b.split(",")) for b in data if b != ""]

blocks = {0:{},1:{},2:{}}
for i in range(3):
    for coord in coords:
        if (coord[i%3], coord[(i+1)%3]) not in blocks[i]:
            blocks[i][(coord[i%3], coord[(i+1)%3])] = set()
        blocks[i][(coord[i%3], coord[(i+1)%3])].add(coord[(i+2)%3])

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

print(count_edges)
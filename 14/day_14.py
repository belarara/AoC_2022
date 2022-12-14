import re, sys
import numpy as np

with open("14/input") as f:
    data = f.read().split("\n")

groups = [[list(map(int, b)) for b in re.findall("(\d+),(\d+)", a)] for a in data if a != ""]

all = []
for g in groups:
    all += g
all_unzip = list(zip(*all))
minx, maxx, miny, maxy = min(all_unzip[0]), max(all_unzip[0]), min(all_unzip[1]), max(all_unzip[1])

qs = np.zeros((maxx+1, maxy+1), dtype=int)
for g in groups:
    for i in range(len(g)-1):
        x1,x2 = g[i][0], g[i+1][0]
        y1,y2 = g[i][1], g[i+1][1]
        valx1, valx2 = (x1,x2) if x1<x2 else (x2,x1)
        valy1, valy2 = (y1,y2) if y1<y2 else (y2,y1)
        if x1 == x2:
            qs[valx1, valy1:valy2+1] = 1
        elif y1 == y2:
            qs[valx1:valx2+1, valy1] = 1

def in_array(ar, pos):
    return pos[0]>=0 and pos[0]<ar.shape[0] and pos[1]>=0 and pos[1]<ar.shape[1]

def next_pos(qs, pos):
    i,j = pos
    next = [(i,j+1), (i-1,j+1), (i+1,j+1)]
    for x in next:
        if not in_array(qs, x):
            return None, False
        if qs[*x]==0:
            return x
    return None, True

def fill_sand(ar, start):
    path = [start]
    ret = True
    while ret:
        i,j = next_pos(ar, path[-1])
        if i is None:
            ret = j
            if j:
                ar[*path[-1]] = 2
                path.pop()
                if len(path)==0:
                    ar[*start] = 2
                    break
        else:
            path.append((i,j))

xs = np.copy(qs)
fill_sand(xs, (500,0))
print(f"1) {np.where(xs==2)[0].shape[0]}")

ys = np.zeros((500+maxy+5,qs.shape[1]+2))
ys[:,-1] = 1
ys[:qs.shape[0],:qs.shape[1]] = np.copy(qs)
fill_sand(ys, (500,0))
print(f"2) {np.where(ys==2)[0].shape[0]}")

if __name__=="__main__" and len(sys.argv)>2:
    from matplotlib import pyplot as plt
    plt.imshow(np.transpose(ys), interpolation='nearest')
    plt.show()

    def print_qs(qs):
        s = ""
        for i in qs:
            for j in i:
                if j==0:
                    s+="."
                elif j==1:
                    s+="#"
                else:
                    s+="o"
            s+="\n"
        return s

    with open("14/output.test", "w") as f:
        f.write(print_qs(np.transpose(ys)))
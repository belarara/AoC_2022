import numpy as np
import heapq

with open("12/input", "r") as f:
    data = [a for a in f.read().split() if a != ""]

ar = np.zeros((len(data),len(data[0])), dtype=int)
for i, line in enumerate(data):
    for j, c in enumerate(line):
        ar[i,j] = ord(c)-ord("a")

start = tuple(np.transpose(np.where(ar==-14))[0])
end = tuple(np.transpose(np.where(ar==-28))[0])
ar[*start] = 0
ar[*end] = ord("z")-ord("a")

def get_children(array, point, f=lambda a, b: a<=b+1):
    i,j = point
    dirs = [(p,q) for p,q in [(i-1,j), (i+1,j), (i,j-1), (i,j+1)] if p>=0 and q>=0 and p<array.shape[0] and q<array.shape[1]]
    val = array[i,j]
    return [a for a in dirs if f(array[*a], val)]

def distance(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

def astar_value(point, steps, end):
    return steps + distance(point,end)

queue = [(astar_value(start,0,end), start, 0)]
heapq.heapify(queue)
visited = {}
while end not in visited:
    _, curr_pos, steps = heapq.heappop(queue)
    if curr_pos not in visited:
        children = get_children(ar, curr_pos)
        visited[curr_pos] = steps
        for c in children:
            if c not in visited:
                heapq.heappush(queue, (astar_value(c, steps+1, end), c, steps+1))
print(f"1) {visited[end]}")

queue = [(astar_value(end, 0, start), end, 0)]
heapq.heapify(queue)
visited = {}
while len(queue)>0:
    _, curr_pos, steps = heapq.heappop(queue)
    if curr_pos not in visited:
        children = get_children(ar, curr_pos, f=lambda a, b: a>=b-1)
        visited[curr_pos] = steps
        for c in children:
            if c not in visited:
                heapq.heappush(queue, (astar_value(c, steps+1, start), c, steps+1))
ls = []
for k,v in visited.items():
    if ar[k] == 0:
        ls.append((v,k))
heapq.heapify(ls)
print(f"2) {heapq.heappop(ls)[0]}")
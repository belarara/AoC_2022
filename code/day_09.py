with open("inputs/09.txt", "r") as f:
    data=f.read().strip()
lines = data.split("\n")

def move_tail(r1,r2):
    (x,y),(xt,yt) = r1, r2
    dx_abs, dy_abs = abs(x-xt), abs(y-yt)
    if dx_abs>1:
        xt = xt-1 if x<xt else xt+1
        if dy_abs>0:
            yt = yt-1 if y<yt else yt+1
    elif dy_abs>1:
        yt = yt-1 if y<yt else yt+1
        if dx_abs>0:
            xt = xt-1 if x<xt else xt+1
    return (xt,yt)

move = {"L":(-1,0), "R":(1,0), "U":(0,-1), "D":(0,1)}
x,y = 0,0
tails = [(0,0)]*9
tail_path1 = [(0,0)]
tail_path2 = [(0,0)]
for k,n in [a.split(" ") for a in lines]:
    n = int(n)
    for l in range(n):
        dx,dy = move[k]
        x,y = x+dx,y+dy
        tails[0] = move_tail((x,y),tails[0])
        for i in range(1,9):
            tails[i] = move_tail(tails[i-1],tails[i])
        tail_path1.append(tails[0])
        tail_path2.append(tails[-1])

print(f"1) {len(list(set(tail_path1)))}")
print(f"2) {len(list(set(tail_path2)))}")
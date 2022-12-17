from collections import deque
import time, sys

fn = "16/input"
if len(sys.argv)>1:
    fn = "16/"+sys.argv[1]
print(fn)

t0 = time.time()
with open(fn) as f:
    data = f.read().split("\n")

valves = {}
for i,d in enumerate([a.split(" ") for a in data if a!=""]):
    valve, flow, conn = d[1], int(d[4][5:-1]), "".join(d[9:]).split(",")
    valves[valve] = {
        "flow": flow,
        "connections": conn,
    }

for i, v in enumerate(sorted(valves.values(), key=lambda q: q["flow"], reverse=True)):
    v["binary"] = 1<<i

binary = {v["binary"]: (v["flow"], [valves[a]["binary"] for a in v["connections"]]) for k,v in valves.items()}

visited = {}
states = [(valves["AA"]["binary"], 0, 0)]
end = 30
for time_step in range(1, end+1):
    new = []
    for valve, opn, total in states:
        if (valve, opn) not in visited or visited[(valve, opn)] < total:
            visited[(valve, opn)] = total
            flow, connections = binary[valve]
            if not valve & opn and flow>0:
                new.append((valve, valve+opn, total + flow*(end - time_step)))
            for conn in connections:
                new.append((conn, opn, total))
    states = new
print(f"1) {max([c for _,_,c in states])}")
t1 = time.time()
print(f"Time: {t1-t0}")

reachable = {}
for k, (flow, conn) in binary.items():
    reachable[k] = {}
    reached = set()
    ls = [(1, a) for a in conn]
    while len(ls)>0:
        d, c = ls.pop(0)
        reached.add(c)
        if binary[c][0]>0:
            reachable[k][c] = d
        ls += [(d+1, a) for a in binary[c][1] if a not in reached and a^k]

has_flow = [k for k,(flow,_) in binary.items() if flow>0]
start_valve = valves["AA"]["binary"]
s = {}
for k,v in valves.items():
    s[v["binary"]] = k

strn = ""
for k,v in reachable.items():
    for o,x in v.items():
        strn += f"{s[k]},{s[o]},{x}\n"

import graphviz

edges = []
g = graphviz.Graph()
g.attr(size='6,6')
for k,d in valves.items():
    for c in d["connections"]:
        if not (k,c) in edges and not (c,k) in edges:
            edges.append((k,c))
for a,b in edges:
    g.edge(a,b)

g.view()


with open("16/output", "w") as f:
    f.write(strn)



print(start_valve)
for k in sorted(reachable.keys(), key=lambda a: s[a]):
    print(f"{s[k]}: ", end="")
    for o in sorted(reachable[k].keys()):
        print(f"{s[o]}, ", end=" ")
    print()

end = 26
states = deque()
for i in has_flow:
    for j in has_flow:
        if i!=j:
            position = (i,j)
            times = (reachable[start_valve][i]+1, reachable[start_valve][j]+1)
            opened = i|j
            pressure = binary[i][0]*(end-(times[0])) + binary[j][0]*(end-(times[1]))
            states.append((position, times, opened, pressure))

visited = {}
end = 26
best_state = 0
counter,modulo = 0, 100000
while len(states)>0:
    counter += 1
    valve, times, opened, pressure = states.popleft()
    #if counter%modulo == 0: print(counter, valve, times, opened, pressure, len(visited), len(states))
    if ((valve[0] | valve[1]), opened) in visited and visited[((valve[0] | valve[1]), opened)] >= pressure:
        continue
    visited[((valve[0] | valve[1]), opened)] = pressure

    is_open = False
    for a in has_flow:
        if not a & opened:
            is_open = True
            break
    if not is_open:
        if best_state<pressure:
            best_state = pressure
        continue

    (valve_me, valve_ele), (time_me, time_ele) = valve, times
    for i in range(2):
        if i==1: (valve_ele, valve_me), (time_ele, time_me) = valve, times
        for cl in has_flow:
            if cl & opened:
                continue
            cost = reachable[valve_me][cl]+1
            steps_to_end = (end - (time_me + cost))
            new_pressure = binary[cl][0]*steps_to_end
            if ((cl | valve_ele), opened) in visited and visited[((cl | valve_ele), opened)] >= pressure+new_pressure:
                continue
            if steps_to_end>0:
                states.append(((valve_ele, cl), (time_ele, time_me+cost), opened|cl, new_pressure + pressure))
            elif best_state<new_pressure+pressure:
                best_state =new_pressure + pressure
        
    #print(valve, times, opened, pressure, new_states)

print(f"2) {best_state}")
t2 = time.time()
print(f"Time: {t2-t1}")
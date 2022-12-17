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
        if c not in reached:
            reached.add(c)
            reachable[k][c] = d
        ls += [(d+1, a) for a in binary[c][1] if a not in reached and a^k]

has_flow = [k for k,(flow,_) in binary.items() if flow>0]
start_valve = valves["AA"]["binary"]

end = 26
states = deque()
states_old = deque()
for i in has_flow:
    for j in has_flow:
        if i!=j:
            position = (i,j)
            times = (reachable[start_valve][i]+1, reachable[start_valve][j]+1)
            opened = i|j
            pressure = binary[i][0]*(end-(times[0])) + binary[j][0]*(end-(times[1]))
            states.append((position, times, opened, pressure, 0))

visual = False # set to true for graph and console output
full_open = sum(has_flow)
visited = {}
best_state = (0,0,0,0,0)
counter = -1
while len(states)>0:
    counter += 1
    valve, times, opened, pressure, ct = states.popleft()
    if visual: states_old.append((valve, times, opened, pressure, ct))
    if best_state[3]<pressure:
        best_state = valve, times, opened, pressure, ct
    if ((valve[0] | valve[1]), opened) in visited and visited[((valve[0] | valve[1]), opened)] >= pressure:
        continue
    visited[((valve[0] | valve[1]), opened)] = pressure
    if not opened ^ full_open:
        continue

    (valve_me, valve_ele), (time_me, time_ele) = valve, times
    for cl in has_flow:
        if cl & opened:
            continue
        cost = reachable[valve_me][cl]+1
        steps_to_end = (end - (time_me + cost))
        new_pressure = binary[cl][0]*steps_to_end
        if ((cl | valve_ele), opened) in visited and visited[((cl | valve_ele), opened)] >= pressure:
            continue
        if best_state[3] <= new_pressure+pressure:
            best_state = ((cl, valve_ele), (time_me+cost, time_ele), opened|cl, new_pressure + pressure, counter)
        if steps_to_end>=0:
            states.append(((cl, valve_ele), (time_me+cost, time_ele), opened|cl, new_pressure + pressure, counter))

    for cl in has_flow:
        if cl & opened:
            continue
        cost = reachable[valve_ele][cl]+1
        steps_to_end = (end - (time_ele + cost))
        new_pressure = binary[cl][0]*steps_to_end
        if ((cl | valve_me), opened) in visited and visited[((cl | valve_me), opened)] >= pressure:
            continue
        if best_state[3] <= new_pressure+pressure:
            best_state = ((valve_me, cl), (time_me, time_ele+cost), opened|cl, new_pressure + pressure, counter)
        if steps_to_end>=0:
            states.append(((valve_me, cl), (time_me, time_ele+cost), opened|cl, new_pressure + pressure, counter))

print(f"2) {best_state[3]}")
t2 = time.time()
print(f"Time: {t2-t1}")

if visual:
    rev = {}
    for k,v in valves.items():
        rev[v["binary"]] = k

    import graphviz

    edges = []
    g = graphviz.Graph()
    g.attr(size='6,6')
    for k,d in valves.items():
        for c in d["connections"]:
            p,q = f"{k}+{d['flow']}", f"{c}+{valves[c]['flow']}"
            if not (p,q) in edges and not (q,p) in edges:
                edges.append((q,p))
    for a,b in edges:
        g.edge(a,b)
    g.view()

    # show best path:
    (pos1, pos2), (ts1, ts2), opened, pressure, counter= best_state
    while counter != 0:
        s1 = f"({rev[pos1]}, {rev[pos2]}) // {(ts1, ts2)}"
        s2 = f"{' '*(20-len(bin(opened)[2:]))}{bin(opened)[2:]} // {pressure}"
        print(f"{s1} // {' '*(40-len(s1))} // {s2}")
        (pos1, pos2), (ts1, ts2), opened, pressure, counter = states_old[counter]
    print(f"({rev[pos1]}, {rev[pos2]}) // {(ts1, ts2)} // {bin(opened)[2:]} // {pressure}")
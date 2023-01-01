from collections import deque
with open("inputs/19.txt", "r") as f:
    data = [a for a in f.read().split("\n") if a!=""]

verbose=False
task_times = (24, 32)
blueprints = {i+1: {} for i in range(len(data))}
for line in data:
    spl = line.split(" ")
    blueprint_number = int(spl[1][:-1])
    blueprints[blueprint_number]["ore"] = (int(spl[6]), 0, 0, 0)
    blueprints[blueprint_number]["clay"] = (int(spl[12]), 0, 0, 0)
    blueprints[blueprint_number]["obsidian"] = (int(spl[18]), int(spl[21]), 0, 0)
    blueprints[blueprint_number]["geode"] = (int(spl[27]), 0, int(spl[30]), 0)

if verbose:
    for bp,v in blueprints.items():
        print(bp,v)

def purchasable(cost, ress):
    if cost[0]<=ress[0] and cost[1]<=ress[1] and cost[2]<=ress[2] and cost[3]<=ress[3]:
        return True
    return False

def next_states(blueprint, state):
    can_buy = (
        purchasable(blueprint["ore"], state[4:8]),
        purchasable(blueprint["clay"], state[4:8]),
        purchasable(blueprint["obsidian"], state[4:8]),
        purchasable(blueprint["geode"], state[4:8]),
    )
    new_state = [a for a in state]
    for i in range(4):
        new_state[4+i] += state[i]
    new_state[8] += 1
    new_states = [tuple(new_state)]
    for i, tp in [(3,"geode"), (2, "obsidian"), (1, "clay"), (0, "ore")]:
        if can_buy[i]:
            new_states.append((
                new_state[0]+int(i==0),
                new_state[1]+int(i==1),
                new_state[2]+int(i==2),
                new_state[3]+int(i==3),
                new_state[4]-blueprint[tp][0],
                new_state[5]-blueprint[tp][1],
                new_state[6]-blueprint[tp][2],
                new_state[7]-blueprint[tp][3],
                new_state[8],
            ))
    return new_states


def generate_gauss_lookup(task_time):
    gauss_lookup = {}
    for i in range(task_time+1):
        for j in range(task_time+1):
            time_left = task_time-j
            if time_left>=0:
                gauss_lookup[(i,j)] = (time_left+1)*i + (pow(time_left, 2)+time_left)//2
    return gauss_lookup

def search_blueprint(blueprint, task_time, prt=False):
    visited = set()
    states = deque([(1,0,0,0,0,0,0,0,0)]) # robo1, robo2, robo3, robo4, ore, clay, obsi, geo, time
    highest_geode = 0
    best_state = (1,0,0,0,0,0,0,0,0)
    count = 0
    gauss_lookup = generate_gauss_lookup(task_time)
    while len(states)>0:
        count+=1
        if prt and count%1000000==0: print(count, len(states))
        current = states.pop()
        if current in visited:
            continue
        visited.add(current)
        if current[7]+gauss_lookup[(current[3],current[8])]<=highest_geode:
            continue
        if current[8] == task_time and current[7]>=highest_geode:
            highest_geode = current[7]
            best_state = current
            continue
        if current[8]<task_time:
            for ns in next_states(blueprint, current):
                states.append(ns)
    return best_state

best_states = {}
for k, bp in blueprints.items():
    best_states[k] = search_blueprint(bp, task_times[0], prt=verbose)
    if verbose: print(f"BLUEPRINT[{k}]: {best_states[k]}")
if verbose: print(best_states)

print(f"1) {sum([k*v[7] for k,v in best_states.items()])}")

best_states_v2 = {}
for k in [1,2,3]:
    if k in blueprints:
        best_states_v2[k] = search_blueprint(blueprints[k], task_times[1], prt=verbose)
        print(best_states_v2[k])
prod = 1
for state in best_states_v2.values():
    prod *= state[7]

print(f"2) {prod}")
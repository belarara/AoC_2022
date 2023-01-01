import sys
from collections import deque

fn = "inputs/17.txt"
if len(sys.argv)>1:
    fn = sys.argv[1]
with open(fn, "r") as f:
    data = [1 if a==">" else -1 for a in f.read() if a in "<>"]
gas_length = len(data)

blocks = {
    1: {(2,0), (3,0), (4,0), (5,0)},
    2: {(3,0), (2,1), (3,1), (4,1), (3,2)},
    3: {(2,0), (3,0), (4,0), (4,1), (4,2)},
    4: {(2,0), (2,1), (2,2), (2,3)},
    5: {(2,0), (2,1), (3,0), (3,1)}
}
field = {i: set() for i in range(1,10)}
area = {1,2,3,4,5,6,7}

def blocked(field, x, y):
    if (x in area) and (y>0) and (x not in field[y]):
        return False
    return True

def print_state(field, area, block_list=[]):
    print()
    print("STATE:")
    for i in sorted(field.keys(), reverse=True):
        for x in sorted(area):
            if (x,i) in block_list:
                print("@", end="")
            elif x not in field[i]:
                print(".", end="")
            else:
                print("#",end="")
        print()

highest = 0
max_field = max(field.keys())
total = 50000
count_blocks = 0
gas_step = 0
queue_pattern = deque()
while count_blocks<total:
    if highest+7 > max_field:
        for i in range(max_field+1, highest+8):
            field[i] = set()
        max_field = highest+7
    count_blocks+=1
    current_block = ((count_blocks-1)%5)+1
    curr_x, curr_y = (1, highest+4)
    falling = True
    while falling:
        gas_is_blocked = False
        for block_x, block_y in blocks[current_block]:
            if blocked(field, curr_x+block_x+data[gas_step], curr_y+block_y):
                gas_is_blocked = True
                break
        if not gas_is_blocked:
            curr_x += data[gas_step]
        gas_step = (gas_step +1) % gas_length
        fall_is_blocked = False
        for block_x, block_y in blocks[current_block]:
            if blocked(field, curr_x+block_x, curr_y+block_y-1):
                fall_is_blocked = True
                break
        if fall_is_blocked:
            queue_pattern.append((current_block, curr_x, curr_y, highest))
            for block_x, block_y in blocks[current_block]:
                field[block_y+curr_y].add(block_x+curr_x)
                if block_y+curr_y>highest:
                    highest = block_y+curr_y
            falling = False
        curr_y -= 1
    if count_blocks == 2022: print(f"1) {highest}") # task1

ls_queue = list(queue_pattern)
rev = list(reversed(ls_queue))
pattern_length = 20
for i in range(pattern_length, len(rev)):
    found_pattern = True
    height_diff = rev[0][2]-rev[pattern_length][2]
    for j in range(pattern_length):
        if (rev[j][0] != rev[pattern_length+j][0] 
        or rev[j][1] != rev[pattern_length+j][1] 
        or rev[j][2]-rev[pattern_length+j][2] != height_diff):
            pattern_length += 1
            found_pattern = False
            break
    if found_pattern:
        break

pattern = ls_queue[-pattern_length:]
pattern_height_diff_table = [(a[3]-ls_queue[-(pattern_length+1)][3]) for a in pattern]
pattern_height = ls_queue[-1][3]-ls_queue[-(pattern_length+1)][3]

pattern_start = None
for i in range(len(ls_queue)):
    found_pattern = True
    for j in range(len(pattern)):
        if (ls_queue[-pattern_length+j][0] != ls_queue[i+j][0]
        or ls_queue[-pattern_length+j][1] != ls_queue[i+j][1]):
            found_pattern = False
            break
    if found_pattern:
        pattern_start = i
        break

pattern_start_height = ls_queue[pattern_start][3]
to_run = 1000000000000
to_repeat = to_run-pattern_start
pattern_repeat = to_repeat//len(pattern)
pattern_left = to_repeat%len(pattern)
height = pattern_start_height + pattern_repeat*pattern_height + pattern_height_diff_table[pattern_left]

print(f"2) {height}")
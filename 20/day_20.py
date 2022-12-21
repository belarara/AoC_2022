with open("20/input", "r") as f:
    data = f.read()
original_list = [int(a) for a in data.split("\n") if a.isdigit() or a[1:].isdigit()]

def perm(ar,per):
    return [ar[per[i]] for i in range(len(per))]

def mix(array, permutation=None):
    length = len(array)
    if permutation is None:
        permutation = {a:a for a in range(length)}
    for i in range(length):
        item = array[i]
        sg = (item>0)-(item<0)
        key = next(iter({k for k,v in permutation.items() if v==i}))
        if sg!=0:
            for j in range(abs(item)%(length-1)):
                current_index = (key+j*sg)%length
                swap_index = (current_index+sg)%length
                permutation[current_index], permutation[swap_index] = permutation[swap_index], permutation[current_index]
    return permutation

task1 = perm(original_list, mix(original_list))
values = [(task1.index(0)+a)%(len(task1)) for a in [1000,2000,3000]]
print(f"1) {sum([task1[v] for v in values])}")

task2 = [(a*811589153) for a in original_list]
permutation = mix(task2)
for i in range(9):
    permutation = mix(task2, permutation)

task2 = perm(task2, permutation)
values = [(task2.index(0)+a)%(len(task2)) for a in [1000,2000,3000]]
print(f"2) {sum([task2[v] for v in values])}")
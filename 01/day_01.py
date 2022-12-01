f = open("01/input", "r")
elfs = []
count = 0
while True:
    line = f.readline()
    if not line:
        elfs.append(count)
        break
    if line == "\n":
        elfs.append(count)
        count = 0
    else:
        count += int(line)
s_elf = sorted(elfs)
print(f"top1: {s_elf[-1]}")
print(f"top3: {sum(s_elf[-3:])}")
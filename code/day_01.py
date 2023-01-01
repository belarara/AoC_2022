f = open("inputs/01.txt", "r")
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
print(f"1) {s_elf[-1]}")
print(f"2) {sum(s_elf[-3:])}")
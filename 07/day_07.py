with open("07/input", "r") as f:
    data=f.read().strip()
lines = data.split("\n")

dirs = {}
current = ""
i = 0
while i<len(lines):
    cmd = lines[i].split(" ")
    if cmd[1] == "cd":
        if cmd[2].startswith("/"):
            current = cmd[2]
        elif cmd[2] == "..":
            current = "/".join(current.split("/")[:-1])
        else:
            current += cmd[2]+"/"
    elif cmd[1] == "ls":
        j = 1
        if current not in dirs:
            dirs[current] = 0
        while i+j<len(lines):
            if not lines[i+j].startswith("$"):
                sp = lines[i+j].split(" ")
                if sp[0].isdigit():
                    dirs[current] += int(sp[0])
                j+=1
            else: 
                break
        i+=j-1
    i+=1

dirs_sub = {}
for key in dirs.keys():
    dirs_sub[key] = sum([v for k,v in dirs.items() if k.startswith(key)])

print(f"1) {sum([v for v in dirs_sub.values() if v<=100000])}")
print(f"2) {min([v for v in dirs_sub.values() if v>=30000000-(70000000-dirs_sub['/'])])}")
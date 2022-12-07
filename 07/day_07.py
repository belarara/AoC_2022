import json
with open("07/input", "r") as f:
    data = f.read()

lines = data.split("\n")

class Dir:
    def __init__(self, parent) -> None:
        self.parent = parent
        if type(parent) is Dir:
            self.parent.children.append(self)
        self.children = []
        self.size = 0
        self.got_size = False

    def get_size(self):
        if not self.got_size:
            for c in self.children:
                self.size += c.get_size()
            self.got_size = True
        return self.size

    def get_children(self):
        children = list(self.children)
        for c in self.children:
            children += c.get_children()
        return children
    
    def print(self, depth):
        print(f"{' '*depth}{self.size}")
        for c in self.children:
            c.print(depth+1)

dir0 = Dir(None)

i = 0
while i<len(lines):
    cmd = lines[i].split(" ")
    if cmd[1] == "cd":
        if cmd[2].startswith("/"):
            curr = dir0
        elif cmd[2] == "..":
            curr = curr.parent
        else:
            curr = Dir(curr)
    elif cmd[1] == "ls":
        #print(f"ls: {cmd}")
        j = 0
        while i+j<len(lines)-1:
            j+=1
            if not lines[i+j].startswith("$"):
                sp = lines[i+j].split(" ")
                print(f"sp {sp}")
                if sp[0].isdigit():
                    curr.size += int(sp[0])
                #print(f"line: {sp}")
            else: 
                break
        i+=j
    i+=1


dir0.get_size()
children = dir0.get_children()
print(children)
print(f"1) {sum([a.get_size() for a in children if a.get_size()<=150000])}")
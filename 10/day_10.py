with open("10/input", "r") as f:
    data=f.readlines()
def pixel(a,b):
    if (a-1)%40 >= b-1 and (a-1)%40 <= b+1:
        return "#"
    return "."

image = ""
cycle,value,total = 1,1,0
for line in data:
    image += pixel(cycle,value)
    cycle+=1
    if cycle%40==20: total +=cycle*value
    if line.startswith("addx"):
        image += pixel(cycle,value)
        value += int(line[5:])
        cycle +=1
        if cycle%40==20: total +=cycle*value

print(f"1) {total}")
print("2)")
for i,e in enumerate(image):
    print(e,end="")
    if i%40==39: print()
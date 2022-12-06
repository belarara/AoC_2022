with open("06/input", "r") as f:
    data = f.read().strip()
found = False
for i,e in enumerate(data):
    if i>2 and len(set(data[i-3:i+1]))==4 and not found:
        print(f"1) {i+1}")
        found = True
    if i>12 and len(set(data[i-13:i+1]))==14:
        print(f"2) {i+1}")
        break
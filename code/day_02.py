f = open("inputs/02.txt", "r")
data = f.read().split("\n")
dct = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}
a = [(dct[i],dct[j]) for i,j in [a.split(" ") for a in data if len(a)==3]]

def get_score(array):
    score=0
    for i,j in array:
        score += j
        if i==j:
            score += 3
        if (i,j) in [(1,2),(2,3),(3,1)]:
            score += 6
    return score

b = []
for i,j in a:
    if j == 1:
        y = ((i-2)%3)+1
    elif j == 2:
        y = i
    elif j == 3:
        y = (i%3)+1
    b.append((i,y))

print(f"1) {get_score(a)}")
print(f"2) {get_score(b)}")
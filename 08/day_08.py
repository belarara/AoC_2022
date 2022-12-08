import numpy as np

with open("08/input", "r") as f:
    data=f.read().strip()

ar = np.array([[int(a) for a in line] for line in data.split("\n")])

z = np.ones(ar.shape)
for i in range(1,ar.shape[0]-1):
    for j in range(1,ar.shape[1]-1):
        if not (ar[i,j]>np.max(ar[:i,j]) or ar[i,j]>np.max(ar[i+1:,j]) or ar[i,j]>np.max(ar[i,:j]) or ar[i,j]>np.max(ar[i,j+1:])):
            z[i,j] = 0
print(f"1) {np.sum(z).astype(int)}")

z21 = np.ones(ar.shape)
z22 = np.ones(ar.shape)
z23 = np.ones(ar.shape)
z24 = np.ones(ar.shape)
for i in range(ar.shape[0]):
    for j in range(ar.shape[1]):
        up = np.flip(ar[:i,j])
        down = ar[i+1:,j]
        left = np.flip(ar[i,:j])
        right = ar[i,j+1:]
        c = 0
        for k,t in enumerate(up):
            z21[i,j] = k+1
            if t>=ar[i,j]:
                break
        for k,t in enumerate(down):
            z22[i,j] = k+1
            c = k
            if t>=ar[i,j]:
                break
        for k,t in enumerate(left):
            z23[i,j] = k+1
            c = k
            if t>=ar[i,j]:
                break
        for k,t in enumerate(right):
            z24[i,j] = k+1
            c = k
            if t>=ar[i,j]:
                break
z2 = np.multiply(np.multiply(z21,z22),np.multiply(z23,z24))
print(f"1) {np.max(z2).astype(int)}")